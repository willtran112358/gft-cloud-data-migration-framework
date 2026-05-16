import sys
import os
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
import boto3
import json
from datetime import timedelta
from pyspark.sql.functions import col
from pyspark.sql.types import StringType, ArrayType

# Accept table_name as a parameter from Step Functions
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'table_name'])
table = args['table_name']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Function to fetch secret from Secrets Manager
def get_postgres_credentials(secret_name):
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

# Load credentials from Secrets Manager
secret_name = "AmazonRDS_data-migration/rds-credentials"
pg_creds = get_postgres_credentials(secret_name)

pg_user = pg_creds.get("user", "postgres")
pg_pass = pg_creds["password"]
pg_host = pg_creds.get("host", "rds-postgress-apse1-uat-data-migration-efea353b98de20ca.ckosc0eaoglw.ap-southeast-1.rds.amazonaws.com")
pg_port = pg_creds.get("port", "5432")
pg_db   = pg_creds.get("database", "postgres")
pg_schema = pg_creds.get("schema", "staging")
s3_raw_bucket = "s3://699955796816-ap-southeast-1-gft-dm-uat-raw"

def column_exists_in_table(table_name, column_name):
    query = f"""
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = '{pg_schema}'
        AND table_name = '{table_name}'
        AND column_name = '{column_name}'
        LIMIT 1
    """
    df = spark.read \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}") \
        .option("query", query) \
        .option("user", pg_user) \
        .option("password", pg_pass) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    return df.count() > 0

def delete_prefix(bucket, prefix, remove_all_versions=False):
    s3 = boto3.resource("s3")
    bucket_res = s3.Bucket(bucket)
    print(f"Scanning {bucket}/{prefix} …")

    if remove_all_versions:
        to_delete = bucket_res.object_versions.filter(Prefix=prefix)
    else:
        to_delete = bucket_res.objects.filter(Prefix=prefix)

    keys = [{"Key": obj.key, **({"VersionId": obj.id} if hasattr(obj, "id") else {})}
            for obj in to_delete]

    if not keys:
        print("Nothing matched that prefix.")
        return

    print(f"Deleting {len(keys)} objects…")
    # Batch in chunks of 1000 (S3 limit per DeleteObjects call)
    client = boto3.client("s3")
    for chunk in [keys[i:i+1000] for i in range(0, len(keys), 1000)]:
        resp = client.delete_objects(Bucket=bucket, Delete={"Objects": chunk})
        if "Errors" in resp:
            print("Some keys failed:", resp["Errors"])
        else:
            print(f"Deleted {len(resp['Deleted'])} keys.")

def get_timestamp_bounds(table: str):
    query = f"SELECT MIN(creation_timestamp) AS min_ts, MAX(creation_timestamp) AS max_ts FROM {pg_schema}.{table}"
    print(query)
    df = spark.read \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}") \
        .option("query", query) \
        .option("user", pg_user) \
        .option("password", pg_pass) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    
    row = df.first()
    if row is None or row["min_ts"] is None or row["max_ts"] is None:
        return None, None
    
    return row["min_ts"], row["max_ts"]

def generate_ranges(min_ts, max_ts, num_parts):
    total_secs = (max_ts - min_ts).total_seconds()
    step = total_secs / num_parts
    ranges = []
    for i in range(num_parts):
        start = min_ts + timedelta(seconds=i * step)
        end = max_ts if i == num_parts - 1 else min_ts + timedelta(seconds=(i + 1) * step)
        ranges.append((start, end))
    return ranges

print(f"\n--- Processing table: {table} ---")
output_path = f"{s3_raw_bucket}/{table}/"
bucket_name = output_path.replace("s3://", "").split("/")[0]
prefix = "/".join(output_path.replace("s3://", "").split("/")[1:])
total_rows_written = 0

try:
    if column_exists_in_table(table, "creation_timestamp"):
        min_ts, max_ts = get_timestamp_bounds(table)
        print(f"Min TS: {min_ts}, Max TS: {max_ts}")

        if min_ts is None or max_ts is None:
            print(f"No usable creation_timestamp data in {table}, skipping.")
            sys.exit(1)

        delete_prefix(bucket_name, prefix)

        if min_ts == max_ts:
            chunk_ranges = [(min_ts, min_ts + timedelta(seconds=1))]
        else:
            chunk_ranges = generate_ranges(min_ts, max_ts, num_parts=3)

        for i, (start, end) in enumerate(chunk_ranges):
            start_str = start.strftime("%Y-%m-%d %H:%M:%S.%f")
            end_str = end.strftime("%Y-%m-%d %H:%M:%S.%f")
            operator = "<=" if i == len(chunk_ranges) - 1 else "<"

            query = f"""
                (SELECT * FROM {pg_schema}.{table}
                 WHERE creation_timestamp >= '{start_str}'
                   AND creation_timestamp {operator} '{end_str}'
                ) AS sub
            """
            print(query)

            df_chunk = spark.read \
                .format("jdbc") \
                .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}") \
                .option("dbtable", query) \
                .option("user", pg_user) \
                .option("password", pg_pass) \
                .option("driver", "org.postgresql.Driver") \
                .load()

            row_count = df_chunk.count()
            print(f"Chunk {i + 1}: {row_count} rows")

            if row_count > 0:
                df_chunk.printSchema()
                df_chunk.show(5, truncate=False)
                df_chunk.write.mode("append").parquet(output_path)
                print(f"Wrote chunk {i + 1} with {row_count} rows to {output_path}")
                total_rows_written += row_count

    else:
        print("Column 'creation_timestamp' not found — exporting full table.")
        delete_prefix(bucket_name, prefix)

        df = spark.read \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}") \
            .option("dbtable", f"{pg_schema}.{table}") \
            .option("user", pg_user) \
            .option("password", pg_pass) \
            .option("driver", "org.postgresql.Driver") \
            .load()

        row_count = df.count()
        print(f"Full table export: {row_count} rows")

        if row_count > 0:
            df = cast_columns_to_string(df)
            df.write.mode("overwrite").parquet(output_path)
            print(f"Wrote full table with {row_count} rows to {output_path}")
            total_rows_written += row_count

    # --- Reconciliation step ---
    if total_rows_written > 0:
        try:
            print(f"\nSuccessfully wrote {total_rows_written} rows for {table}")

            # Step 1: Query row count from PostgreSQL
            print("Querying row count from PostgreSQL...")
            pg_row_count_df = spark.read \
                .format("jdbc") \
                .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}") \
                .option("dbtable", f"(SELECT COUNT(*) AS row_count FROM {pg_schema}.{table}) AS row_count_table") \
                .option("user", pg_user) \
                .option("password", pg_pass) \
                .option("driver", "org.postgresql.Driver") \
                .load()

            source_row_count = pg_row_count_df.collect()[0]["row_count"]
            print(f"Source PostgreSQL row count: {source_row_count}")

            # Step 2: Read back from S3
            print("Reading back from S3 for reconciliation...")
            df_s3 = spark.read.parquet(output_path)
            s3_row_count = df_s3.count()
            print(f"S3 row count: {s3_row_count}")

            if s3_row_count != total_rows_written or s3_row_count != source_row_count:
                raise Exception(
                    f"Reconciliation failed:\n"
                    f"  Source (PostgreSQL): {source_row_count}\n"
                    f"  Written: {total_rows_written}\n"
                    f"  Read Back (S3): {s3_row_count}"
                )

            print("Reconciliation passed. All counts match!")
            print(f"Table: {table}, Source: {source_row_count}, Written: {total_rows_written}, S3: {s3_row_count}")
        except Exception as recon_err:
            print(f"Reconciliation failed: {recon_err}")
            raise
    else:
        raise Exception(f"No data written for {table}. Job failed intentionally to alert operator.")

    job.commit()

except Exception as e:
    print(f"Error processing {table}: {e}")
    raise
