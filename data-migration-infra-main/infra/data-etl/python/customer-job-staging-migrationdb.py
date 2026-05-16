import sys
import traceback
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame, DynamicFrameCollection
from awsgluedq.transforms import EvaluateDataQuality
from pyspark.sql.functions import col, lit, concat_ws

# ----------------------------
# Custom Transform Function
# ----------------------------
def MyTransform(glueContext, dfc, entity="customer") -> DynamicFrameCollection:
    args = getResolvedOptions(sys.argv, ['execution_id'])
    execution_id = args['execution_id']
    # last_part = execution_id.split(':')[-1]
    last_part = 'Manual_Execution'

    print(f"execution_id: {execution_id}")
    print(f"global_migration_id: {last_part}")
    print(f"entity: {entity}")

    # Get Spark DataFrame
    df = dfc.select(list(dfc.keys())[0]).toDF()

    # Add required columns
    df = df.withColumn("entity", lit(entity)) \
           .withColumn("global_migration_id", lit(last_part))

    # Safe rule handling
    dq_columns = {
        "DataQualityRulesPass": "rules_pass",
        "DataQualityRulesFail": "rules_fail",
        "DataQualityRulesSkip": "rules_skip"
    }

    for dq_col, new_col in dq_columns.items():
        if dq_col in df.columns:
            df = df.withColumn(new_col, concat_ws(", ", col(dq_col)))
        else:
            print(f"Column {dq_col} not found in DataFrame — setting {new_col} = None")
            df = df.withColumn(new_col, lit(None))

    # Debug output
    df.printSchema()
    df.show(5, truncate=False)

    # Return as DynamicFrameCollection
    transformed = DynamicFrame.fromDF(df, glueContext, "dynamic_frame_transformed")
    return DynamicFrameCollection({"customTransform0": transformed}, glueContext)

# ----------------------------
# Spark SQL Wrapper
# ----------------------------
def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

# ----------------------------
# Glue Job Init
# ----------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'execution_id'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

try:
    print("Starting Glue job for customer...")

    # Load from staging (drop duplicates)
    df_source = glueContext.create_data_frame.from_catalog(
        database="uat_staging",
        table_name="customer"
    )
    dyf = DynamicFrame.fromDF(df_source.dropDuplicates(), glueContext, "dyf")

    # Filter for valid IDs
    dyf_filtered = sparkSqlQuery(
        glueContext,
        "SELECT * FROM myDataSource WHERE id IS NOT NULL",
        {"myDataSource": dyf},
        "dyf_filtered"
    )

    # Define DQ rules
    dq_rules = """
    Rules = [
        ColumnLength "id" <= 36,
        IsUnique "id",
        IsComplete "id"
    ]
    """

    dq_result = EvaluateDataQuality().process_rows(
        frame=dyf_filtered,
        ruleset=dq_rules,
        publishing_options={
            "dataQualityEvaluationContext": "dq_results",
            "enableDataQualityCloudWatchMetrics": True,
            "enableDataQualityResultsPublishing": True
        },
        additional_options={"performanceTuning.caching": "CACHE_NOTHING"}
    )

    # Extract outcomes
    outcomes = SelectFromCollection.apply(dfc=dq_result, key="rowLevelOutcomes")

    # Split passed and all rows
    all_rows = sparkSqlQuery(glueContext, "SELECT * FROM myDataSource", {"myDataSource": outcomes}, "all_rows")
    pass_rows = sparkSqlQuery(
        glueContext,
        "SELECT * FROM myDataSource WHERE DataQualityEvaluationResult NOT LIKE 'Failed'",
        {"myDataSource": outcomes},
        "pass_rows"
    )

    # Enrich with metadata
    transformed_all = MyTransform(glueContext, DynamicFrameCollection({"input": all_rows}, glueContext), entity="customer")
    transformed_pass = MyTransform(glueContext, DynamicFrameCollection({"input": pass_rows}, glueContext), entity="customer")

    all_final = SelectFromCollection.apply(transformed_all, key="customTransform0")
    pass_final = SelectFromCollection.apply(transformed_pass, key="customTransform0")

    # Rename DQ result column for fail tracking
    renamed_dq_fails = RenameField.apply(
        all_final, old_name="DataQualityEvaluationResult", new_name="result"
    )

    # Map fail schema for logging
    mapped_dq_fails = ApplyMapping.apply(
        frame=renamed_dq_fails,
        mappings=[
            ("id", "string", "id", "string"),
            ("global_migration_id", "string", "global_migration_id", "string"),
            ("entity", "string", "entity", "string"),
            ("rules_pass", "string", "rules_pass", "string"),
            ("rules_fail", "string", "rules_fail", "string"),
            ("rules_skip", "string", "rules_skip", "string"),
            ("result", "string", "result", "string")
        ]
    )

    # Write passing rows to Iceberg
    df_pass = pass_final.toDF().select("id", "global_migration_id")
    print(f"Writing {df_pass.count()} passing records to Iceberg: glue_catalog.uat_migrationdb.customer")
    df_pass.writeTo("glue_catalog.uat_migrationdb.customer").append()

    # Write DQ fail logs to staging
    glueContext.write_dynamic_frame.from_catalog(
        frame=mapped_dq_fails,
        database="uat_staging",
        table_name="dq_fails"
    )

    job.commit()
    print("Glue job completed successfully.")

except Exception as e:
    print("\nGlue job failed with exception:")
    traceback.print_exc()
    raise
