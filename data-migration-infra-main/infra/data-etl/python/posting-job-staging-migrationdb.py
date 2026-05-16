import sys
import traceback
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame, DynamicFrameCollection
from awsgluedq.transforms import EvaluateDataQuality
from pyspark.sql.functions import col, lit, concat_ws, when

# --- Custom transform for adding metadata and rule columns ---
def MyTransform(glueContext, dfc, entity="posting") -> DynamicFrameCollection:
    args = getResolvedOptions(sys.argv, ['execution_id'])
    execution_id = args['execution_id']
    last_part = 'Manual_Execution'  # Or: execution_id.split(':')[-1]

    df = dfc.select(list(dfc.keys())[0]).toDF()

    df = df.withColumn("entity", lit(entity)) \
           .withColumn("global_migration_id", lit(last_part))

    dq_columns = {
        "DataQualityRulesPass": "rules_pass",
        "DataQualityRulesFail": "rules_fail",
        "DataQualityRulesSkip": "rules_skip"
    }

    for dq_col, new_col in dq_columns.items():
        if dq_col in df.columns:
            df = df.withColumn(new_col, concat_ws(", ", col(dq_col)))
        else:
            print(f"Missing {dq_col}, setting {new_col} to None")
            df = df.withColumn(new_col, lit(None))

    df.printSchema()
    df.show(5, truncate=False)

    transformed = DynamicFrame.fromDF(df, glueContext, "dynamic_frame_transformed")
    return DynamicFrameCollection({"customTransform0": transformed}, glueContext)

# --- Helper for running SQL on DynamicFrame ---
def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

# --- Job Initialization ---
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'execution_id'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

try:
    print("Starting Glue job for posting...")

    # Correct: Read Iceberg table as Spark DataFrame
    print("Reading from Iceberg table: uat_staging.posting")
    df_staging = glueContext.create_data_frame.from_catalog(
        database="uat_staging",
        table_name="posting"
    ).dropDuplicates()

    # Convert to DynamicFrame for DQ
    dyf_staging = DynamicFrame.fromDF(df_staging, glueContext, "dyf_staging")

    # Data Quality Rules
    dq_rules = """
    Rules = [
        IsComplete "client_id",
        IsComplete "target_account_id"
    ]
    """
    dq_results = EvaluateDataQuality().process_rows(
        frame=dyf_staging,
        ruleset=dq_rules,
        publishing_options={
            "dataQualityEvaluationContext": "dq_results",
            "enableDataQualityCloudWatchMetrics": True,
            "enableDataQualityResultsPublishing": True
        },
        additional_options={"performanceTuning.caching": "CACHE_NOTHING"}
    )

    # Extract passed & all DQ outcomes
    row_level_outcomes = SelectFromCollection.apply(dfc=dq_results, key="rowLevelOutcomes")

    dyf_all = sparkSqlQuery(
        glueContext, "SELECT * FROM myDataSource",
        {"myDataSource": row_level_outcomes}, "dyf_all"
    )

    dyf_passed = sparkSqlQuery(
        glueContext,
        "SELECT * FROM myDataSource WHERE DataQualityEvaluationResult NOT LIKE 'Failed'",
        {"myDataSource": row_level_outcomes},
        "dyf_passed"
    )

    # Add metadata columns
    all_transformed = MyTransform(glueContext, DynamicFrameCollection({"input": dyf_all}, glueContext))
    passed_transformed = MyTransform(glueContext, DynamicFrameCollection({"input": dyf_passed}, glueContext))

    all_final = SelectFromCollection.apply(all_transformed, key="customTransform0")
    passed_final = SelectFromCollection.apply(passed_transformed, key="customTransform0")

    # Rename result field for failed records
    dq_fail_renamed = RenameField.apply(all_final, old_name="DataQualityEvaluationResult", new_name="result")

    # Map DQ fail columns for Glue table logging
    mapped_dq_fails = ApplyMapping.apply(
        frame=dq_fail_renamed,
        mappings=[
            ("client_transaction_id", "string", "id", "string"),
            ("global_migration_id", "string", "global_migration_id", "string"),
            ("entity", "string", "entity", "string"),
            ("rules_pass", "string", "rules_pass", "string"),
            ("rules_fail", "string", "rules_fail", "string"),
            ("rules_skip", "string", "rules_skip", "string"),
            ("result", "string", "result", "string")
        ]
    )

    # Only select needed columns for Iceberg write
    expected_columns = [
        "client_id",
        "client_batch_id",
        "target_account_id",
        "batch_details",
        "posting_instruction"
    ]

    df_posting = passed_final.toDF().select(*expected_columns)

    print(f"Writing {df_posting.count()} records to Iceberg table: aux_posting_instruction_batch")
    df_posting.writeTo("glue_catalog.uat_migrationdb.aux_posting_instruction_batch").append()
    print("Successfully wrote to Iceberg")

    # Log DQ failures
    print("Logging DQ fails to Glue table: dq_fails")
    glueContext.write_dynamic_frame.from_catalog(
        frame=mapped_dq_fails,
        database="uat_staging",
        table_name="dq_fails"
    )
    print("Successfully logged DQ fails")

    job.commit()
    print("Glue job completed successfully.")

except Exception as e:
    print("\nGlue job failed with exception:")
    traceback.print_exc()
    raise
