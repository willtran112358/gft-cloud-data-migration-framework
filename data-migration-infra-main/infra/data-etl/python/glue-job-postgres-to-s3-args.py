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



# Accept table_name as a parameter from Step Functions
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'table_name', 'pg_host', 'pg_port', 'pg_user', 'pg_secret_name', 'pg_database', 'pg_schema', 'output_s3'])

print(args)
table = args['table_name']
pg_host = args['pg_host']
pg_port = args['pg_port']
pg_user = args['pg_user']
pg_secret_name = args['pg_secret_name']
pg_database = args['pg_database']
pg_schema = args['pg_schema']
output_s3 = args['output_s3']

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
# secret_name = "AmazonRDS_data-migration/rds-credentials"
pg_creds = get_postgres_credentials(pg_secret_name)

pg_user = pg_creds.get("user", pg_user)
pg_pass = pg_creds["password"]
pg_host = pg_creds.get("host", pg_host)
pg_port = pg_creds.get("port", pg_port)
pg_db   = pg_creds.get("database", pg_database)
pg_schema = pg_creds.get("schema", pg_schema)  # default to 'staging'
# s3_raw_bucket = "s3://699955796816-ap-southeast-1-gft-dm-uat-raw"
s3_raw_bucket = output_s3

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

def delete_existing_s3_objects(bucket, prefix):
    s3 = boto3.resource("s3")
    bucket_obj = s3.Bucket(bucket)
    print(f"Deleting all objects under {bucket}/{prefix}")
    bucket_obj.objects.filter(Prefix=prefix).delete()

def get_timestamp_bounds(table: str):
    """
    Fetch min and max creation_timestamp from a table
    """
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
    return row["min_ts"], row["max_ts"]

# Split range into chunks
def generate_ranges(min_ts, max_ts, num_parts):
    total_secs = (max_ts - min_ts).total_seconds()
    step = total_secs / num_parts
    ranges = []

    for i in range(num_parts):
        start = min_ts + timedelta(seconds=i * step)
        end = min_ts + timedelta(seconds=(i + 1) * step)
        ranges.append((start, end))

    return ranges

print(f"\n--- Processing table: {table} ---")
output_path = f"{s3_raw_bucket}/{table}/"
bucket_name = output_path.replace("s3://", "").split("/")[0]
prefix = "/".join(output_path.replace("s3://", "").split("/")[1:])
try:
    if column_exists_in_table(table, "creation_timestamp"):
        min_ts, max_ts = get_timestamp_bounds(table)
        print(f"Min TS: {min_ts}, Max TS: {max_ts}")

        if min_ts is None or max_ts is None:
            print(f"No creation_timestamp field in {table}, skipping.")
            sys.exit(1)

        print(f"Min: {min_ts}, Max: {max_ts}")

        delete_existing_s3_objects(bucket_name, prefix)

        chunk_ranges = generate_ranges(min_ts, max_ts, num_parts=3)

        for i, (start, end) in enumerate(chunk_ranges):
            print(f"\nReading chunk {i + 1}: {start} to {end}")

            query = f"""
                (SELECT * FROM {pg_schema}.{table}
                WHERE creation_timestamp >= '{start}'
                AND creation_timestamp < '{end}') AS sub
            """

            df_chunk = spark.read \
                .format("jdbc") \
                .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}") \
                .option("dbtable", query) \
                .option("user", pg_user) \
                .option("password", pg_pass) \
                .option("driver", "org.postgresql.Driver") \
                .load()

            # Append to raw zone
            df_chunk.write.mode("append").parquet(output_path)
            print(f"Wrote chunk {i + 1} to {output_path}")
    else:
        print("Column 'creation_timestamp' not found — exporting full table.")
        df = spark.read \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}") \
            .option("dbtable", f"{pg_schema}.{table}") \
            .option("user", pg_user) \
            .option("password", pg_pass) \
            .option("driver", "org.postgresql.Driver") \
            .load()

        df.write.mode("overwrite").parquet(output_path)

    print(f"\nSuccessfully processed and wrote all chunks for {table}")
    job.commit()

except Exception as e:
    print(f"Error processing {table}: {e}")
    raise



