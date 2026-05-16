import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    struct, col, collect_list, to_json, lit, create_map, map_from_arrays, array, expr, udf, map_from_entries, coalesce
)
from pyspark.sql.types import *
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

columns_parameter_values_to_cast = [
    ("effective_interest_rate", DecimalType(12, 4)),
    ("minimum_balance", DecimalType(12, 4)),
    ("minimum_balance_after_partial_withdrawal", DecimalType(12, 4)),
    ("minimum_initial_deposit", DecimalType(12, 4)),
    ("minimum_partial_withdrawal_amount", DecimalType(12, 4)),
    ('proposed_deposit_amount', DecimalType(12, 4)),
    ('withdrawal_amount', DecimalType(12, 4))
]

columns_withdrawal_to_cast = [
    ("amount", DecimalType(12, 4))  # Cast 'amount' to DecimalType(12, 2)
]

# Function to fix timestamp precision
def truncate_timestamps(df):
    for col_name in ["source_create_timestamp", "source_open_timestamp", "source_close_timestamp"]:
        if col_name in df.columns:
            df = df.withColumn(
                col_name,
                expr(f"from_unixtime(round(unix_timestamp({col_name}) * 1000) / 1000)")
            )
    return df

if table == "sa_account":
    account_df = spark.read.format("parquet").load(f"{raw_base_path}/account/")

    if "creation_timestamp" in account_df.columns:
        account_df = account_df.drop("creation_timestamp")

    account_df = truncate_timestamps(account_df)

    parameter_df = spark.read.format("parquet").load(f"{raw_base_path}/parameter_values_sa/")

    for column_name, decimal_type in columns_parameter_values_to_cast:
        parameter_df = parameter_df.withColumn(column_name, parameter_df[column_name].cast(decimal_type))

    blockade_df = spark.read.format("parquet").load(f"{raw_base_path}/blockade_sa/")

    withdrawal_tracker_sa_df = spark.read.format("parquet").load(f"{raw_base_path}/withdrawal_tracker_sa/")

    for column_name, decimal_type in columns_withdrawal_to_cast:
        withdrawal_tracker_sa_df =  withdrawal_tracker_sa_df.withColumn(column_name, withdrawal_tracker_sa_df[column_name].cast(decimal_type))


    # Parameter type mapping
    param_type_map = {
        "account_status_requested_by": "enumeration_value",
        "accrual_precision": "decimal_value",
        "add_on_principal_days_before_maturity": "decimal_value",
        "add_on_principal_during_tenure": "enumeration_value",
        "add_on_principal_on_maturity_day": "enumeration_value",
        "adjusted_interest_day": "decimal_value",
        "application_precision": "decimal_value",
        "branch_internal_account": "string_value",
        "customer_nominated_account": "string_value",
        "days_in_year": "enumeration_value",
        "denomination": "string_value",
        "deposit_non_term_interest_code": "string_value",
        "desired_maturity_date": "string_value",
        "early_partial_withdrawal_allowed": "enumeration_value",
        "effective_interest_rate": "decimal_value",
        "immediate_interest_date": "string_value",
        "interest_application_frequency": "enumeration_value",
        "interest_application_type": "enumeration_value",
        "interest_resolve_type": "string_value",
        "minimum_balance": "decimal_value",
        "minimum_balance_after_partial_withdrawal": "decimal_value",
        "minimum_initial_deposit": "decimal_value",
        "minimum_partial_withdrawal_amount": "decimal_value",
        "multiple_deposit_allowed": "enumeration_value",
        "new_interest_rate_update_method": "enumeration_value",
        "number_of_days_to_end_reminder_return_withdrawal": "decimal_value",
        "number_of_days_to_start_reminder_return_withdrawal": "decimal_value",
        "proposed_deposit_amount": "decimal_value",
        "rollover_option": "enumeration_value",
        "savings_account_status": "enumeration_value",
        "term_start_date": "string_value",
        "withdrawal_amount": "decimal_value"
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

    withdrawal_map_df = withdrawal_tracker_sa_df.groupBy("parameter_values_id").agg(
        map_from_entries(
            collect_list(
                struct(
                    col("withdrawal_date").cast("string"),
                    col("amount").cast("string")
                )
            )
        ).alias("withdrawal_tracker_map")
    )

    parameter_with_blockades = parameter_df.join(
        blockade_struct,
        parameter_df.id == blockade_struct.parameter_values_id,
        how="left"
    ).join(
        withdrawal_map_df,
        parameter_df.id == withdrawal_map_df.parameter_values_id,
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
    outer_values.append(
        create_map(lit("string_value"), coalesce(col("blockade_json"), lit("[]")))
    )

    outer_keys.append(lit("withdrawal_tracker"))
    outer_values.append(
        create_map(lit("string_value"), coalesce(to_json(col("withdrawal_tracker_map")), lit("{}")))
    )


    # Final parameter_values JSON column
    parameter_json_df = parameter_with_blockades.withColumn(
        "parameter_values",
        to_json(map_from_arrays(array(*outer_keys), array(*outer_values)))
    ).select("account_id", "parameter_values")

    final_account_df = account_df.join(
        parameter_json_df,
        account_df.id == parameter_json_df.account_id
    ).drop("account_id")

    final_account_df = truncate_timestamps(final_account_df)

    final_account_df.printSchema()
    final_account_df.writeTo(f"{catalog_base}.account").append()

else:
    raise ValueError(f"Unsupported table: {table}")

job.commit()
