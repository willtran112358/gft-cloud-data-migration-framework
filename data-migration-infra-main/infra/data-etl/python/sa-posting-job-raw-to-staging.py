import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    struct, col, collect_list, to_json, lit, create_map, map_from_arrays, array, expr, udf, coalesce
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
                        daily_interest_amount_tracker,
                        accrued_demand_interest_payable, applied_interest_tracker, pending_cash_out,
                        effective_interest_rate, application_date):

    def posting(credit, amount, address, acc_id, denomination="VND", asset="COMMERCIAL_BANK_MONEY"):
        return {
            "credit": credit,
            "amount": str(amount),
            "denomination": denomination,
            "account_id": str(acc_id),
            "account_address": str(address),
            "asset": asset,
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
    if daily_interest_amount_tracker != 0:
        postings.append(posting(daily_interest_amount_tracker > 0, daily_interest_amount_tracker, "DAILY_INTEREST_AMOUNT_TRACKER", target_account_id))

    # Block 5
    if accrued_demand_interest_payable != 0:
        postings.append(posting(accrued_demand_interest_payable > 0, accrued_demand_interest_payable, "ACCRUED_DEMAND_INTEREST_PAYABLE", target_account_id))

    # Block 6
    if applied_interest_tracker != 0:
        postings.append(posting(applied_interest_tracker > 0, applied_interest_tracker, "APPLIED_INTEREST_TRACKER", target_account_id))

    # Block 7
    if pending_cash_out != 0:
        postings.append(posting(pending_cash_out > 0, pending_cash_out, "PENDING_CASH_OUT", target_account_id))

    # Block 8
    total = accrued_interest_payable + daily_interest_amount_tracker + accrued_demand_interest_payable + applied_interest_tracker + pending_cash_out
    if total != 0:
        postings.append(posting(total < 0, total, "INTERNAL_CONTRA", target_account_id))

    # Block 9
    total_1 = effective_interest_rate
    if total_1 != 0:
        postings.append(posting(total_1 < 0, total_1, "INTERNAL_CONTRA", target_account_id, "RATE", "PRODUCT_CONFIGURATION"))

    # Block 10 & 11 (compare with null-safe logic)
    if application_date != 0:
        postings.append(posting(application_date > 0, application_date, "APPLICATION_DATE", target_account_id, "DATE", "EVENT_TRACKER"))
        postings.append(posting(application_date < 0, application_date, "INTERNAL_CONTRA", target_account_id, "DATE", "EVENT_TRACKER"))

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

if table == "sa_posting":
    posting_df = (
        spark.read.format("parquet")
        .load(f"{raw_base_path}/posting_instruction_batch/")
    )

    if "creation_timestamp" in posting_df.columns:
        posting_df = posting_df.drop("creation_timestamp")
    posting_df = truncate_timestamps(posting_df)

    balances_sa_df = spark.read.format("parquet").load(f"{raw_base_path}/balances_sa/")
    
    # Show schemas
    print("posting_df schema:")
    posting_df.printSchema()

    print("balances_sa_df schema:")
    balances_sa_df.printSchema()


    joined_df = posting_df.alias("pib") \
        .join(balances_sa_df.alias("b"), col("pib.id") == col("b.posting_instruction_batch_id"))
    

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
            col("b.daily_interest_amount_tracker").cast("double"),
            col("b.accrued_interest_payable").cast("double"),
            col("b.applied_interest_tracker").cast("double"),
            col("b.pending_cash_out").cast("double"),
            col("b.effective_interest_rate").cast("double"),
            col("b.application_date").cast("double")
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
