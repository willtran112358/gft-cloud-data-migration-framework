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

    final_json = {
        "client_id": client_id,
        "client_batch_id": client_batch_id,
        "target_account_id": target_account_id,
        "batch_details": {
            "global_reconciliator_id": "Manual_Execution",
            "account_id": target_account_id,
            "context": "migration"
        },
        "posting_instructions": [
            {
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
            }
        ]
    }

    return json.dumps(final_json)


# Function to fix timestamp precision
def truncate_timestamps(df):
    for col_name in ["source_create_timestamp", "source_open_timestamp", "source_close_timestamp"]:
        if col_name in df.columns:
            df = df.withColumn(
                col_name,
                expr(f"from_unixtime(round(unix_timestamp({col_name}) * 1000) / 1000)")
            )
    return df

if table == "customer":
    df = spark.read.format("parquet").load(f"{raw_base_path}/customer/")
    if "creation_timestamp" in df.columns:
        df = df.drop("creation_timestamp")
    df = truncate_timestamps(df)
    df.writeTo(f"{catalog_base}.customer").append()

elif table == "ca_account":
    account_df = spark.read.format("parquet").load(f"{raw_base_path}/account/")
    if "creation_timestamp" in account_df.columns:
        account_df = account_df.drop("creation_timestamp")
    account_df = truncate_timestamps(account_df)

    parameter_df = spark.read.format("parquet").load(f"{raw_base_path}/parameter_values_ca/")
    blockade_df = spark.read.format("parquet").load(f"{raw_base_path}/blockade_ca/")

    # Parameter type mapping
    param_type_map = {
        "accrual_precision": "decimal_value",
        "application_precision": "decimal_value",
        "denomination": "string_value",
        "deposit_non_term_interest_code": "string_value",
        "interest_application_day": "decimal_value",
        "interest_application_frequency": "enumeration_value",
        "interest_resolve_type": "string_value",
        "margin_interest_rate": "decimal_value",
        "minimum_balance": "decimal_value",
        "minimum_balance_requirement": "decimal_value",
        "overdraft_account_id": "string_value",
        "overdraft_original_limit": "decimal_value",
        "overdraft_limit_block": "enumeration_value",
        "account_status_requested_by": "enumeration_value",
        "apply_interest_and_skip_end_of_day": "enumeration_value"
    }

    # Aggregate blockades into JSON array
    blockade_struct = blockade_df.groupBy("parameter_values_id").agg(
        to_json(collect_list(struct(
            col("blockade_id"),
            col("start"),
            col("end"),
            col("block_amount")
        ))).alias("blockade_json")
    )

    parameter_with_blockades = parameter_df.join(
        blockade_struct,
        parameter_df.id == blockade_struct.parameter_values_id,
        how="left"
    )

    # Build outer map of field -> {wrapper: value}
    outer_keys = []
    outer_values = []

    for field, wrapper in param_type_map.items():
        outer_keys.append(lit(field))
        outer_values.append(create_map(lit(wrapper), col(field).cast("string")))

    # Add blockade field
    outer_keys.append(lit("blockade"))
    outer_values.append(create_map(lit("string_value"), col("blockade_json")))

    # Final parameter_values JSON column
    parameter_json_df = parameter_with_blockades.withColumn(
        "parameter_values",
        to_json(map_from_arrays(array(*outer_keys), array(*outer_values)))
    ).select("account_id", "parameter_values")

    # Join to account and write
    final_account_df = account_df.join(
        parameter_json_df,
        account_df.id == parameter_json_df.account_id,
        how="left"
    ).drop("account_id")

    final_account_df = truncate_timestamps(final_account_df)

    final_account_df.printSchema()
    final_account_df.writeTo(f"{catalog_base}.account").append()

elif table == "ca_posting":
    posting_df = (
        spark.read.format("parquet")
        .load(f"{raw_base_path}/posting_instruction_batch/")
        .where(col("client_transaction_id").isNotNull())
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
        .join(balances_ca_df.alias("b"), col("pib.id") == col("b.posting_instruction_batch_id")) \
    

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
