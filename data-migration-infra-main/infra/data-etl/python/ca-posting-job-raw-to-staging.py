import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    struct, col, collect_list, to_json, lit, create_map, map_from_arrays, array, expr, udf
)
from pyspark.sql.types import StringType
import json

# Parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'table_name'])
table = args['table_name']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Common S3 base path
raw_base_path = "s3://699955796816-ap-southeast-1-gft-dm-uat-raw"
catalog_base = "glue_catalog.uat_staging"

def build_postings_json(client_id, client_batch_id, client_transaction_id,
                        target_account_id, denomination,
                        default_balance, accrued_interest_payable,
                        inactive_day_count, utlised_overdraft):

    def posting(credit, amount, address, acc_id):
        return {
            "credit": credit,
            "amount": str(amount),
            "denomination": denomination,
            "account_id": str(acc_id),
            "account_address": str(address),
            "asset": "COMMERCIAL_BANK_MONEY",
            "phase": "POSTING_PHASE_COMMITTED"
        }

    postings = []

    # Block 1 & 2
    if default_balance != 0:
        postings.append(posting(default_balance > 0, default_balance, "DEFAULT", target_account_id))
        postings.append(posting(default_balance < 0, default_balance, "DEFAULT", "branch_internal_account"))

    # Block 3
    if accrued_interest_payable != 0:
        postings.append(posting(accrued_interest_payable > 0, accrued_interest_payable, "ACCRUED_INTEREST_PAYABLE", target_account_id))

    # Block 4
    if inactive_day_count != 0:
        postings.append(posting(inactive_day_count > 0, inactive_day_count, "INACTIVE_DAY_COUNT", target_account_id))

    # Block 5
    if utlised_overdraft != 0:
        postings.append(posting(utlised_overdraft > 0, utlised_overdraft, "UTILISED_OVERDRAFT", target_account_id))

    # Block 6
    total = accrued_interest_payable + inactive_day_count + utlised_overdraft
    if total != 0:
        postings.append(posting(total < 0, total, "INTERNAL_CONTRA", target_account_id))

    # Return only posting_instructions list (not full batch)
    return json.dumps({
        "client_transaction_id": client_transaction_id,
        "custom_instruction": {
            "postings": postings
        },
        "instruction_details": {
            "originating_account_id": target_account_id
        },
        "override": {
            "restrictions": {
                "all": True,
                "restriction_set_ids": []
            }
        }
    })



# Function to fix timestamp precision
def truncate_timestamps(df):
    for col_name in ["source_create_timestamp", "source_open_timestamp", "source_close_timestamp"]:
        if col_name in df.columns:
            df = df.withColumn(
                col_name,
                expr(f"from_unixtime(round(unix_timestamp({col_name}) * 1000) / 1000)")
            )
    return df

if table == "ca_posting":
    posting_df = (
        spark.read.format("parquet")
        .load(f"{raw_base_path}/posting_instruction_batch/")
        .where(col("client_transaction_id").isNotNull())
        .where(col("target_account_id").isNotNull())
    )


    if "creation_timestamp" in posting_df.columns:
        posting_df = posting_df.drop("creation_timestamp")
    posting_df = truncate_timestamps(posting_df)

    balances_ca_df = spark.read.format("parquet").load(f"{raw_base_path}/balances_ca/")

    
    # Show schemas
    print("posting_df schema:")
    posting_df.printSchema()

    print("balances_ca_df schema:")
    balances_ca_df.printSchema()


    joined_df = posting_df.alias("pib") \
        .join(balances_ca_df.alias("b"), col("pib.id") == col("b.posting_instruction_batch_id"))
    

    print("Successfully joined all dataframes.")

    joined_df.show(5, truncate=False)

    build_postings_udf = udf(build_postings_json, StringType())

    final_posting_df = joined_df.withColumn(
        "posting_instruction",
        build_postings_udf(
            col("pib.client_id"),
            col("pib.client_batch_id"),
            col("pib.client_transaction_id"),
            col("pib.target_account_id"),
            col("pib.denomination"),
            col("b.default_balance").cast("double"),
            col("b.accrued_interest_payable").cast("double"),
            col("b.inactive_day_count").cast("double"),
            col("b.utlised_overdraft").cast("double"),
        )
    )

    final_posting_df = final_posting_df.withColumn(
        "batch_details",
        to_json(struct(
            lit("Manual_Execution").alias("global_reconciliator_id"),
            col("pib.target_account_id").alias("account_id"),
            lit("migration").alias("context")
        ))
    )

    # Select final output
    final_posting_df = final_posting_df.select(
        col("pib.client_id"),
        col("pib.client_batch_id"),
        col("pib.target_account_id"),
        "posting_instruction",
        "batch_details"
    )

    print("Final DataFrame schema:")
    final_posting_df.printSchema()

    print(f"Total records: {final_posting_df.count()}")
   

    final_posting_df.writeTo(f"{catalog_base}.posting").append()


else:
    raise ValueError(f"Unsupported table: {table}")

job.commit()
