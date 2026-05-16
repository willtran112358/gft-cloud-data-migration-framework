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
# raw_base_path = args['raw_base_path']
# catalog_base = args['catalog_base']
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Common S3 base path
raw_base_path = "s3://699955796816-ap-southeast-1-gft-dm-uat-raw"
catalog_base = "glue_catalog.uat_staging"
def build_od_postings_json(client_id, client_batch_id, client_transaction_id,
                           target_account_id, denomination,
                           default_balance,
                           principal,
                           accrued_interest_receivable,
                           due_interest,
                           due_principal,
                           overdue_interest,
                           interest_penalty_tracked,
                           interest_penalty_accrued,
                           interest_penalty_applied,
                           overdue_principal,
                           principal_penalty_tracked,
                           principal_penalty_accrued,
                           principal_penalty_applied,
                           adhoc_due_interest_tracker,
                           chargeable_accrued_interest_penalty,
                           chargeable_accrued_interest,
                           chargeable_accrued_principal_penalty,
                           aggregate_balance
                           ):
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

    if default_balance != 0:
        postings.append(posting(default_balance < 0, default_balance, "DEFAULT", target_account_id))
        postings.append(posting(default_balance > 0, default_balance, "DEFAULT", "branch_internal_account"))

    if principal != 0:
        postings.append(posting(principal < 0, principal, "PRINCIPAL", target_account_id))
    
    if accrued_interest_receivable != 0:
        postings.append(posting(accrued_interest_receivable < 0, accrued_interest_receivable, "ACCRUED_INTEREST_RECEIVABLE", target_account_id))

    if due_interest != 0:
        postings.append(posting(due_interest < 0, due_interest, "DUE_INTEREST", target_account_id))

    if due_principal != 0:
        postings.append(posting(due_principal < 0, due_principal, "DUE_PRINCIPAL", target_account_id))

    if overdue_interest != 0:
        postings.append(posting(overdue_interest < 0, overdue_interest, "OVERDUE_INTEREST", target_account_id))

    if overdue_principal != 0:
        postings.append(posting(overdue_principal < 0, overdue_principal, "OVERDUE_PRINCIPAL", target_account_id))

    if interest_penalty_tracked != 0:
        postings.append(posting(interest_penalty_tracked < 0, interest_penalty_tracked, "INTEREST_PENALTY_TRACKED", target_account_id))

    if interest_penalty_accrued != 0:
        postings.append(posting(interest_penalty_accrued < 0, interest_penalty_accrued, "INTEREST_PENALTY_ACCRUED", target_account_id))

    if interest_penalty_applied != 0:
        postings.append(posting(interest_penalty_applied < 0, interest_penalty_applied, "INTEREST_PENALTY_APPLIED", target_account_id))

    if principal_penalty_tracked != 0:
        postings.append(posting(principal_penalty_tracked < 0, principal_penalty_tracked, "PRINCIPAL_PENALTY_TRACKED", target_account_id))

    if principal_penalty_accrued != 0:
        postings.append(posting(principal_penalty_accrued < 0, principal_penalty_accrued, "PRINCIPAL_PENALTY_ACCRUED", target_account_id))

    if principal_penalty_applied != 0:
        postings.append(posting(principal_penalty_applied < 0, principal_penalty_applied, "PRINCIPAL_PENALTY_APPLIED", target_account_id))

    if adhoc_due_interest_tracker != 0:
        postings.append(posting(adhoc_due_interest_tracker < 0, adhoc_due_interest_tracker, "ADHOC_DUE_INTEREST_TRACKER", target_account_id))

    if chargeable_accrued_interest_penalty != 0:
        postings.append(posting(chargeable_accrued_interest_penalty < 0, chargeable_accrued_interest_penalty, "CHARGEABLE_ACCRUED_PRINCIPAL_PENALTY", target_account_id))

    if chargeable_accrued_interest != 0:
        postings.append(posting(chargeable_accrued_interest < 0, chargeable_accrued_interest, "CHARGEABLE_ACCRUED_INTEREST", target_account_id))

    if chargeable_accrued_principal_penalty != 0:
        postings.append(posting(chargeable_accrued_principal_penalty < 0, chargeable_accrued_principal_penalty, "CHARGEABLE_ACCRUED_INTEREST_PENALTY", target_account_id))
    
    if aggregate_balance != 0:
        postings.append(posting(aggregate_balance < 0, aggregate_balance, "AGGREGATE_BALANCE",
                                target_account_id))

    # Block 6
    total_list = [principal, accrued_interest_receivable, due_interest, due_principal, overdue_interest, overdue_principal, interest_penalty_tracked, interest_penalty_accrued, interest_penalty_applied, principal_penalty_tracked, principal_penalty_accrued, principal_penalty_applied, adhoc_due_interest_tracker, chargeable_accrued_principal_penalty, chargeable_accrued_interest, chargeable_accrued_interest_penalty, aggregate_balance]

    total = sum(x or 0 for x in total_list)

    if total != 0:
        postings.append(posting(total > 0, total, "INTERNAL_CONTRA", target_account_id))

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


if table == 'od_posting':
    posting_df = (
        spark.read.format("parquet")
        .load(f"{raw_base_path}/posting_instruction_batch/")
    )

    if "creation_timestamp" in posting_df.columns:
        posting_df = posting_df.drop("creation_timestamp")
    posting_df = truncate_timestamps(posting_df)

    balances_od_df = spark.read.format("parquet").load(f"{raw_base_path}/balances_od/")

    # Show schemas
    print("posting_df schema:")
    posting_df.printSchema()

    print("balances_od_df schema:")
    balances_od_df.printSchema()

    joined_df = posting_df.alias("pib").join(balances_od_df.alias("b"),
                                             col("pib.id") == col("b.posting_instruction_batch_id"))

    print("Successfully joined all dataframes.")

    joined_df.show(5, truncate=False)

    build_postings_udf = udf(build_od_postings_json, StringType())

    final_posting_df = joined_df.withColumn(
        "posting_instruction",
        build_postings_udf(
            col("pib.client_id"),
            col("pib.client_batch_id"),
            col("pib.client_transaction_id"),
            col("pib.target_account_id"),
            col("pib.denomination"),
            col("b.default_balance").cast("double"),
            col("b.principal").cast("double"),
            col("b.accrued_interest_receivable").cast("double"),
            col("b.due_interest").cast("double"),
            col("b.due_principal").cast("double"),
            col("b.overdue_interest").cast("double"),
            col("b.interest_penalty_tracked").cast("double"),
            col("b.interest_penalty_accrued").cast("double"),
            col("b.interest_penalty_applied").cast("double"),
            col("b.overdue_principal").cast("double"),
            col("b.principal_penalty_tracked").cast("double"),
            col("b.principal_penalty_accrued").cast("double"),
            col("b.principal_penalty_applied").cast("double"),
            col("b.adhoc_due_interest_tracker").cast("double"),
            col("b.chargeable_accrued_interest_penalty").cast("double"),
            col("b.chargeable_accrued_interest").cast("double"),
            col("b.chargeable_accrued_principal_penalty").cast("double"),
            col("b.aggregate_balance").cast("double"),
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
    print(f"final_posting_df")
    
    print(f"Total records: {final_posting_df.count()}")

    final_posting_df.writeTo(f"{catalog_base}.posting").append()

else:
    raise ValueError(f"Unsupported table: {table}")

job.commit()
