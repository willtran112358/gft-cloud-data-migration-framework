import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    struct, col, collect_list, to_json, lit, create_map, map_from_arrays, array, expr, to_date, coalesce
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

raw_base_path = "s3://699955796816-ap-southeast-1-gft-dm-uat-raw"
catalog_base = "glue_catalog.uat_staging"

# Function to fix timestamp precision
def truncate_timestamps(df):
    for col_name in ["source_create_timestamp", "source_open_timestamp", "source_close_timestamp"]:
        if col_name in df.columns:
            df = df.withColumn(
                col_name,
                expr(f"from_unixtime(round(unix_timestamp({col_name}) * 1000) / 1000)")
            )
    return df

columns_parameter_values_to_cast = [
    ("maximum_interest_rate", DecimalType(12, 4)),
    ("minimum_interest_rate", DecimalType(12, 4)),
    ("penalty_interest_rate", DecimalType(12, 4)),
    ("penalty_principal_rate_multiplier", DecimalType(12, 4))
]

columns_interest_to_cast = [
    ("rate", DecimalType(12, 4)) 
]

if table == "od_account":
    account_df = spark.read.format("parquet").load(f"{raw_base_path}/account/")
    if "creation_timestamp" in account_df.columns:
        account_df = account_df.drop("creation_timestamp")
    account_df = truncate_timestamps(account_df)

    parameter_df = spark.read.format("parquet").load(f"{raw_base_path}/parameter_values_od/")
    
    for column_name, decimal_type in columns_parameter_values_to_cast:
        parameter_df = parameter_df.withColumn(column_name, parameter_df[column_name].cast(decimal_type))
    
    fixed_interest_rate = spark.read.format("parquet").load(f"{raw_base_path}/fixed_interest_rate_od/")
    
    for column_name, decimal_type in columns_interest_to_cast:
        fixed_interest_rate =  fixed_interest_rate.withColumn(column_name, fixed_interest_rate[column_name].cast(decimal_type))

    fixed_interest_rate_json = fixed_interest_rate.select(
        "parameter_values_id",
        to_json(
            struct(col("start_date"), col("end_date"), col("rate"))
        ).alias("fixed_interest_rate_json")
    )

    original_due_interest_days = spark.read.format("parquet").load(f"{raw_base_path}/original_due_interest_dates_od/")

    original_due_interest_days = original_due_interest_days.withColumn("due_date_parsed", to_date("due_date", "yyyy-MM-dd"))

    sorted_df = original_due_interest_days.orderBy("parameter_values_id", "due_date_parsed")

    original_due_interest_days_struct = sorted_df.groupBy("parameter_values_id").agg(
        to_json(collect_list(col("due_date"))).alias("due_interest_dates_json")
    )

    parameter_with_interest_rates = parameter_df.join(
        fixed_interest_rate_json,
        parameter_df.id == fixed_interest_rate_json.parameter_values_id
    )

    complete_parameters = parameter_with_interest_rates.join(
        original_due_interest_days_struct,
        parameter_df.id == original_due_interest_days_struct.parameter_values_id
    )

    param_type_map = {
        "accrual_precision": "decimal_value",
        "denomination": "string_value",
        "original_maturity_date": "string_value",
        "penalty_interest_rate": "decimal_value",
        "write_off": "enumeration_value",
        "penalty_principal_rate_multiplier": "decimal_value",
        "debt_group": "decimal_value",
        "fixed_interest_term": "decimal_value",
        "application_precision": "decimal_value",
        "minimum_interest_rate": "decimal_value",
        "maximum_interest_rate": "decimal_value",
        "interest_repayment_method": "enumeration_value",
        "days_in_year": "enumeration_value",
        "grace_period_for_interest": "decimal_value",
        "start_from_actual_due_date": "enumeration_value",
        "current_account_id": "string_value"
    }

    # Build outer map of field -> {wrapper: value}
    outer_keys = []
    outer_values = []

    for field, wrapper in param_type_map.items():
        outer_keys.append(lit(field))
        outer_values.append(create_map(lit(wrapper), col(field).cast("string")))
    
    # Add blockade field
    outer_keys.append(lit("fixed_interest_rate"))
    outer_values.append(create_map(lit("string_value"), coalesce(col("fixed_interest_rate_json"), lit("{}"))))

    outer_keys.append(lit("original_due_interest_dates"))
    outer_values.append(create_map(lit("string_value"), coalesce(col("due_interest_dates_json"), lit("[]"))))

    parameter_json_df = complete_parameters.withColumn(
        "parameter_values",
        to_json(map_from_arrays(array(*outer_keys), array(*outer_values)))
    ).select("account_id", "parameter_values")

    # Join to account and write
    final_account_df = account_df.join(
        parameter_json_df,
        account_df.id == parameter_json_df.account_id,
    ).drop("account_id")

    final_account_df = truncate_timestamps(final_account_df)

    final_account_df.printSchema()
    final_account_df.writeTo(f"{catalog_base}.account").append()
else:
    raise ValueError(f"Unsupported table: {table}")

job.commit()
