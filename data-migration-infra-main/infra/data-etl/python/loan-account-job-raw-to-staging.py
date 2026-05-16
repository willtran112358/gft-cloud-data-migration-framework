import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    struct, col, collect_list, to_json, lit, create_map, map_from_arrays, array, expr, to_date, coalesce
)
from pyspark.sql.types import (
    StructType, StructField, StringType, ArrayType, TimestampType, IntegerType, DecimalType, DoubleType
)

# Parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Common S3 base path
raw_base_path = "s3://699955796816-ap-southeast-1-gft-dm-uat-raw"
catalog_base = "glue_catalog.uat_staging"

# Function to fix timestamp precision
def truncate_timestamps(df):
    timestamp_cols = ["source_create_timestamp", "source_open_timestamp"]
    for col_name in timestamp_cols:
        if col_name in df.columns:
            df = df.withColumn(
                col_name,
                expr(f"from_unixtime(round(unix_timestamp({col_name}) * 1000) / 1000)")
            )
    return df

# Define columns to cast
columns_parameter_values_to_cast = [
    ("maximum_interest_rate", DecimalType(12, 4)),
    ("minimum_interest_rate", DecimalType(12, 4)),
    ("penalty_interest_rate", DecimalType(12, 4)),
    ("penalty_principal_rate_multiplier", DecimalType(12, 4)),
    ("principal", DecimalType(12, 4))
]

columns_interest_to_cast = [
    ("rate", DecimalType(12, 4))
]

columns_auto_rollover_to_cast = [
    ("spread_rate", DecimalType(12, 4))
]

columns_due_principal_to_cast = [
    ("due_principal_amount", DecimalType(12, 4))
]

# Read account data (main table) with explicit schema
account_df = spark.read.format("parquet").load(f"{raw_base_path}/account/")
if "creation_timestamp" in account_df.columns:
    account_df = account_df.drop("creation_timestamp")

# Read loan-specific parameter tables with explicit schemas
parameter_df = spark.read.format("parquet").load(f"{raw_base_path}/parameter_values_loan/")
auto_rollover_df = spark.read.format("parquet").load(f"{raw_base_path}/auto_rollover_interest_schedule_plan_loan/")
fixed_interest_df = spark.read.format("parquet").load(f"{raw_base_path}/fixed_interest_rate_loan/")
due_interest_df = spark.read.format("parquet").load(f"{raw_base_path}/original_due_interest_dates_loan/")
due_principal_df = spark.read.format("parquet").load(f"{raw_base_path}/original_due_principal_records_loan/")

# Cast columns to appropriate types
for column_name, decimal_type in columns_parameter_values_to_cast:
    parameter_df = parameter_df.withColumn(column_name, parameter_df[column_name].cast(decimal_type))

for column_name, decimal_type in columns_interest_to_cast:
    fixed_interest_df = fixed_interest_df.withColumn(column_name, fixed_interest_df[column_name].cast(decimal_type))

for column_name, decimal_type in columns_auto_rollover_to_cast:
    auto_rollover_df = auto_rollover_df.withColumn(column_name, auto_rollover_df[column_name].cast(decimal_type))

for column_name, decimal_type in columns_due_principal_to_cast:
    due_principal_df = due_principal_df.withColumn(column_name, due_principal_df[column_name].cast(decimal_type))

# Debug: Inspect auto_rollover_df after casting
print("Schema of auto_rollover_df after casting:")
auto_rollover_df.printSchema()
auto_rollover_df.show(5, truncate=False)

# Parameter type mapping based on provided feedback
param_type_map = {
    "accrual_precision": "decimal_value",
    "application_precision": "decimal_value",
    "days_in_year": "enumeration_value",
    "debt_group": "decimal_value",
    "denomination": "string_value",
    "disbursement_account": "string_value",
    "fixed_interest_term": "decimal_value",
    "grace_period_for_interest": "decimal_value",
    "grace_period_for_principal": "decimal_value",
    "interest_repayment_method": "enumeration_value",
    "maximum_interest_rate": "decimal_value",
    "minimum_interest_rate": "decimal_value",
    "original_maturity_date": "string_value",
    "penalty_interest_rate": "decimal_value",
    "penalty_principal_rate_multiplier": "decimal_value",
    "principal": "decimal_value",
    "start_from_actual_due_date": "enumeration_value",
    "write_off": "enumeration_value"
}

# Aggregate auto_rollover_interest_schedule_plan_loan into JSON array
auto_rollover_struct = auto_rollover_df.groupBy("parameter_values_id").agg(
    to_json(
        collect_list(
            struct(
                col("base_rate_code"),
                col("spread_rate"),
                col("update_date")
            )
        )
    ).alias("auto_rollover_json")
)

# Aggregate fixed_interest_rate_loan into JSON array
fixed_interest_struct = fixed_interest_df.groupBy("parameter_values_id").agg(
    to_json(
        collect_list(
            struct(
                col("start_date"),
                col("end_date"),
                col("rate")
            )
        )
    ).alias("fixed_interest_json")
)

# Aggregate original_due_interest_dates_loan into JSON array of dates with explicit sorting
due_interest_df = due_interest_df.withColumn("due_date_parsed", to_date("due_date", "yyyy-MM-dd"))
sorted_due_interest_df = due_interest_df.orderBy("parameter_values_id", "due_date_parsed")
due_interest_struct = sorted_due_interest_df.groupBy("parameter_values_id").agg(
    to_json(
        collect_list(
            col("due_date")
        )
    ).alias("due_interest_json")
)

# Aggregate original_due_principal_records_loan into JSON array
due_principal_struct = due_principal_df.groupBy("parameter_values_id").agg(
    to_json(
        collect_list(
            struct(
                col("due_principal_amount"),
                col("original_due_principal_date")
            )
        )
    ).alias("due_principal_json")
)

# Join all aggregated structures to parameter_values_loan
parameter_with_agg = parameter_df.join(
    auto_rollover_struct,
    parameter_df.id == auto_rollover_struct.parameter_values_id,
    how="left"
).join(
    fixed_interest_struct,
    parameter_df.id == fixed_interest_struct.parameter_values_id,
    how="left"
).join(
    due_interest_struct,
    parameter_df.id == due_interest_struct.parameter_values_id,
    how="left"
).join(
    due_principal_struct,
    parameter_df.id == due_principal_struct.parameter_values_id,
    how="left"
)

# Build outer map of field -> {wrapper: value}
outer_keys = []
outer_values = []

for field, wrapper in param_type_map.items():
    outer_keys.append(lit(field))
    outer_values.append(create_map(lit(wrapper), col(field).cast("string")))

# Add aggregated fields
agg_fields = [
    ("auto_rollover_interest_schedule_plan", "auto_rollover_json"),
    ("fixed_interest_rate", "fixed_interest_json"),
    ("original_due_interest_dates", "due_interest_json"),
    ("original_due_principal_records", "due_principal_json")
]

for field_name, col_name in agg_fields:
    outer_keys.append(lit(field_name))
    default_value = lit("[]") if col_name != "due_principal_json" else lit("{}")
    outer_values.append(create_map(lit("string_value"), coalesce(col(col_name), default_value)))

# Final parameter_values JSON column
parameter_json_df = parameter_with_agg.withColumn(
    "parameter_values",
    to_json(map_from_arrays(array(*outer_keys), array(*outer_values)))
).select("account_id", "parameter_values")

# Join to account and prepare final DataFrame
final_account_df = account_df.join(
    parameter_json_df,
    account_df.id == parameter_json_df.account_id,
    how="inner"
).drop("account_id")

# Truncate timestamps
final_account_df = truncate_timestamps(final_account_df)

# Filter for loan accounts (optional)
final_account_df = final_account_df.where(col("parameter_values").isNotNull())

# Print schema and sample output for verification
final_account_df.printSchema()
final_account_df.show(5, truncate=False)

# Write to Iceberg table in Glue Catalog (append mode)
final_account_df.writeTo(f"{catalog_base}.loan_account").append()

# Commit job
job.commit()