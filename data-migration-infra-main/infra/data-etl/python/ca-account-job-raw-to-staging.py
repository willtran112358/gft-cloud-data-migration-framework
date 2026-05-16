import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    struct, col, collect_list, to_json, lit, create_map, map_from_arrays, array, expr, udf, coalesce
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

columns_to_cast = [
    ("margin_interest_rate", DecimalType(12, 4)),
    ("minimum_balance", DecimalType(12, 4)),
    ("minimum_balance_requirement", DecimalType(12, 4)),
    ("overdraft_original_limit", DecimalType(12, 4))
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

if table == "ca_account":
    account_df = spark.read.format("parquet").load(f"{raw_base_path}/account/") 

    if "creation_timestamp" in account_df.columns:
        account_df = account_df.drop("creation_timestamp")
    account_df = truncate_timestamps(account_df)

    parameter_df = spark.read.format("parquet").load(f"{raw_base_path}/parameter_values_ca/")
    for column_name, decimal_type in columns_to_cast:
        parameter_df = parameter_df.withColumn(column_name, parameter_df[column_name].cast(decimal_type))

    blockade_df = spark.read.format("parquet").load(f"{raw_base_path}/blockade_ca/")

    # Parameter type mapping
    param_type_map = {
        "accrual_precision": "decimal_value",
        "application_precision": "decimal_value",
        "apply_interest_and_skip_end_of_day": "enumeration_value",
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
        "account_status_requested_by": "enumeration_value"
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
    outer_values.append(
        create_map(lit("string_value"), coalesce(col("blockade_json"), lit("[]")))
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
