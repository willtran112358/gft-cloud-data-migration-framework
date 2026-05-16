import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    struct, col, to_json, lit, expr, udf
)
from pyspark.sql.types import StringType
import json
import boto3

# Parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'table_name'])
table = args['table_name']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

raw_base_path = "s3://699955796816-ap-southeast-1-gft-dm-uat-raw"
catalog_base = "glue_catalog.uat_staging"

# Function to check if S3 path contains .parquet files
def check_s3_path_exists(s3_path):
    s3_client = boto3.client('s3')
    bucket, prefix = s3_path.replace("s3://", "").split("/", 1)
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if 'Contents' not in response:
        return False
    for obj in response['Contents']:
        if obj['Key'].endswith('.parquet'):
            return True
    return False

# Log contents of an S3 path
def log_s3_path_contents(s3_path):
    s3_client = boto3.client('s3')
    bucket, prefix = s3_path.replace("s3://", "").split("/", 1)
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if 'Contents' not in response:
        print(f"No objects found in {s3_path}")
        return
    print(f"Objects in {s3_path}:")
    for obj in response['Contents']:
        print(f" - {obj['Key']} (Size: {obj['Size']} bytes)")

# UDF logic for building JSON posting instructions
def build_loan_postings_json(
    client_id, client_batch_id, client_transaction_id, target_account_id, denomination,
    default_balance, original_principal, principal, accrued_interest_receivable,
    due_interest, due_principal, overdue_interest, overdue_principal, interest_penalty_tracked,
    interest_penalty_accrued, interest_penalty_applied, principal_penalty_tracked, principal_penalty_accrued, principal_penalty_applied,
    fixed_interest_type_repaid_tracker, fixed_total_interest_amount_tracker, interest_accrual_adjustment_tracker, adhoc_due_interest_tracker,
    chargeable_accrued_principal_penalty, chargeable_accrued_interest, chargeable_accrued_interest_penalty,
    aggregate_balance, base_interest_rate
):
    try:
        def posting(credit, amount, address, acc_id, asset="COMMERCIAL_BANK_MONEY", denomination="VND"):
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
            postings.append(posting(default_balance < 0, default_balance, "DEFAULT", target_account_id))
            postings.append(posting(default_balance > 0, default_balance, "DEFAULT", "branch_internal_account"))

        # Block 3
        if original_principal != 0:
            postings.append(posting(original_principal < 0, original_principal, "ORIGINAL_PRINCIPAL", target_account_id))

        # Block 4
        if principal != 0:
            postings.append(posting(principal < 0, principal, "PRINCIPAL", target_account_id))

        # Block 5
        if accrued_interest_receivable != 0:
            postings.append(posting(accrued_interest_receivable < 0, accrued_interest_receivable, "ACCRUED_INTEREST_RECEIVABLE", target_account_id))

        # Block 6
        if due_interest != 0:
            postings.append(posting(due_interest < 0, due_interest, "DUE_INTEREST", target_account_id))

        # Block 7
        if due_principal != 0:
            postings.append(posting(due_principal < 0, due_principal, "DUE_PRINCIPAL", target_account_id))

        # Block 8
        if overdue_interest != 0:
            postings.append(posting(overdue_interest < 0, overdue_interest, "OVERDUE_INTEREST", target_account_id))

        # Block 9
        if overdue_principal != 0:
            postings.append(posting(overdue_principal < 0, overdue_principal, "OVERDUE_PRINCIPAL", target_account_id))

        # Block 10
        if interest_penalty_tracked != 0:
            postings.append(posting(interest_penalty_tracked < 0, interest_penalty_tracked, "INTEREST_PENALTY_TRACKED", target_account_id))

        # Block 11
        if interest_penalty_accrued != 0:
            postings.append(posting(interest_penalty_accrued < 0, interest_penalty_accrued, "INTEREST_PENALTY_ACCRUED", target_account_id))

        # Block 12
        if interest_penalty_applied != 0:
            postings.append(posting(interest_penalty_applied < 0, interest_penalty_applied, "INTEREST_PENALTY_APPLIED", target_account_id))

        # Block 13
        if principal_penalty_tracked != 0:
            postings.append(posting(principal_penalty_tracked < 0, principal_penalty_tracked, "PRINCIPAL_PENALTY_TRACKED", target_account_id))

        # Block 14
        if principal_penalty_accrued != 0:
            postings.append(posting(principal_penalty_accrued < 0, principal_penalty_accrued, "PRINCIPAL_PENALTY_ACCRUED", target_account_id))

        # Block 15
        if principal_penalty_applied != 0:
            postings.append(posting(principal_penalty_applied < 0, principal_penalty_applied, "PRINCIPAL_PENALTY_APPLIED", target_account_id))

        # Block 16
        if fixed_interest_type_repaid_tracker != 0:
            postings.append(posting(fixed_interest_type_repaid_tracker < 0, fixed_interest_type_repaid_tracker, "FIXED_INTEREST_TYPE_REPAID_TRACKER", target_account_id))

        # Block 17
        if fixed_total_interest_amount_tracker != 0:
            postings.append(posting(fixed_total_interest_amount_tracker < 0, fixed_total_interest_amount_tracker, "FIXED_TOTAL_INTEREST_AMOUNT_TRACKER", target_account_id))

        # Block 18
        if interest_accrual_adjustment_tracker != 0:
            postings.append(posting(interest_accrual_adjustment_tracker < 0, interest_accrual_adjustment_tracker, "INTEREST_ACCRUAL_ADJUSTMENT_TRACKER", target_account_id))

        # Block 19
        if adhoc_due_interest_tracker != 0:
            postings.append(posting(adhoc_due_interest_tracker < 0, adhoc_due_interest_tracker, "ADHOC_DUE_INTEREST_TRACKER", target_account_id))

        # Block 20
        if chargeable_accrued_principal_penalty != 0:
            postings.append(posting(chargeable_accrued_principal_penalty < 0, chargeable_accrued_principal_penalty, "CHARGEABLE_ACCRUED_PRINCIPAL_PENALTY", target_account_id))

        # Block 21
        if chargeable_accrued_interest != 0:
            postings.append(posting(chargeable_accrued_interest < 0, chargeable_accrued_interest, "CHARGEABLE_ACCRUED_INTEREST", target_account_id))

        # Block 22
        if chargeable_accrued_interest_penalty != 0:
            postings.append(posting(chargeable_accrued_interest_penalty < 0, chargeable_accrued_interest_penalty, "CHARGEABLE_ACCRUED_INTEREST_PENALTY", target_account_id))

        # Block 23
        if aggregate_balance != 0:
            postings.append(posting(aggregate_balance < 0, aggregate_balance, "AGGREGATE_BALANCE", target_account_id))

        total = sum(x or 0 for x in [
            original_principal, principal, accrued_interest_receivable, due_interest, due_principal,
            overdue_interest, overdue_principal, interest_penalty_tracked, interest_penalty_accrued,
            interest_penalty_applied, principal_penalty_tracked, principal_penalty_accrued, principal_penalty_applied,
            fixed_interest_type_repaid_tracker, fixed_total_interest_amount_tracker, interest_accrual_adjustment_tracker,
            adhoc_due_interest_tracker, chargeable_accrued_principal_penalty, chargeable_accrued_interest,
            chargeable_accrued_interest_penalty, aggregate_balance
        ])

        # Block 24
        if total != 0:
            postings.append(posting(total > 0, total, "INTERNAL_CONTRA", target_account_id))

        # Block 25 & 26
        if base_interest_rate != 0:
            postings.append(posting(base_interest_rate < 0, base_interest_rate, "BASE_INTEREST_RATE", target_account_id, "PRODUCT_CONFIGURATION", "RATE"))
            postings.append(posting(base_interest_rate > 0, base_interest_rate, "INTERNAL_CONTRA", target_account_id, "PRODUCT_CONFIGURATION", "RATE"))

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

    except Exception as e:
        return json.dumps({"error": str(e), "client_transaction_id": str(client_transaction_id)})

# Fix timestamp precision
def truncate_timestamps(df):
    for col_name in ["source_create_timestamp", "source_open_timestamp", "source_close_timestamp"]:
        if col_name in df.columns:
            df = df.withColumn(
                col_name,
                expr(f"from_unixtime(round(unix_timestamp({col_name}) * 1000) / 1000)")
            )
    return df

# ========== MAIN LOGIC ==========
if table  == "loan_posting":
    posting_path = f"{raw_base_path}/posting_instruction_batch/"
    log_s3_path_contents(posting_path)

    if not check_s3_path_exists(posting_path):
        print(f"No .parquet files found in {posting_path}. No data to process.")
        job.commit()
    else:
        posting_df = spark.read.format("parquet").load(posting_path)
        if "creation_timestamp" in posting_df.columns:
            posting_df = posting_df.drop("creation_timestamp")
        posting_df = truncate_timestamps(posting_df)

        if posting_df.rdd.isEmpty():
            print("No rows in posting_df. Exiting job.")
            job.commit()
        else:
            balances_path = f"{raw_base_path}/balances_loan/"
            log_s3_path_contents(balances_path)

            if not check_s3_path_exists(balances_path):
                print(f"No .parquet files found in {balances_path}. No data to process.")
                job.commit()
            else:
                balances_loan_df = spark.read.format("parquet").load(balances_path)

                if balances_loan_df.rdd.isEmpty():
                    print("No rows in balances_loan_df. Exiting job.")
                    job.commit()
                else:
                    joined_df = posting_df.alias("pib").join(
                        balances_loan_df.alias("b"),
                        col("pib.id") == col("b.posting_instruction_batch_id")
                    )

                    if joined_df.rdd.isEmpty():
                        print("No rows after join. Exiting job.")
                        job.commit()
                    else:
                        build_postings_udf = udf(build_loan_postings_json, StringType())
                        final_posting_df = joined_df.withColumn(
                            "posting_instruction",
                            build_postings_udf(
                                col("pib.client_id"),
                                col("pib.client_batch_id"),
                                col("pib.client_transaction_id"),
                                col("pib.target_account_id"),
                                col("pib.denomination"),
                                *[col(f"b.{field}").cast("double") for field in [
                                    "default_balance", "original_principal", "principal", "accrued_interest_receivable",
                                    "due_interest", "due_principal", "overdue_interest", "overdue_principal",
                                    "interest_penalty_tracked", "interest_penalty_accrued", "interest_penalty_applied",
                                    "principal_penalty_tracked", "principal_penalty_accrued", "principal_penalty_applied",
                                    "fixed_interest_type_repaid_tracker", "fixed_total_interest_amount_tracker",
                                    "interest_accrual_adjustment_tracker", "adhoc_due_interest_tracker",
                                    "chargeable_accrued_principal_penalty", "chargeable_accrued_interest",
                                    "chargeable_accrued_interest_penalty", "aggregate_balance", "base_interest_rate"
                                ]]
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
