import sys
import traceback
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection, DynamicFrame
from awsgluedq.transforms import EvaluateDataQuality
from pyspark.sql.functions import col, lit, concat_ws

# Custom Transform to enrich rows
def MyTransform(glueContext, dfc, entity="account") -> DynamicFrameCollection:


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

# Spark SQL wrapper
def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

# Main job setup
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'execution_id'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

try:
    print("Starting Glue job...")

    # Load from staging table
    print("Reading from uat_staging.account...")
    raw_df = glueContext.create_data_frame.from_catalog(
        database="uat_staging",
        table_name="account"
    )
    raw_dyf = DynamicFrame.fromDF(raw_df, glueContext, "raw_dyf")

    # Drop duplicates
    deduped_dyf = DynamicFrame.fromDF(
        raw_dyf.toDF().dropDuplicates(),
        glueContext,
        "deduped"
    )
    print(f" Deduplicated record count: {deduped_dyf.count()}")

    # Filter rows where id is not null
    filtered_dyf = sparkSqlQuery(
        glueContext,
        "SELECT * FROM myDataSource WHERE id IS NOT NULL",
        {"myDataSource": deduped_dyf},
        "filtered_dyf"
    )
    print(f"Filtered record count: {filtered_dyf.count()}")

    # Evaluate Data Quality
    print("Running Data Quality evaluation...")
    dq_rules = """
        Rules = [
            IsComplete "id"
        ]
    """
    dq_results = EvaluateDataQuality().process_rows(
        frame=filtered_dyf,
        ruleset=dq_rules,
        publishing_options={
            "dataQualityEvaluationContext": "dq_results",
            "enableDataQualityCloudWatchMetrics": True,
            "enableDataQualityResultsPublishing": True
        },
        additional_options={"performanceTuning.caching": "CACHE_NOTHING"}
    )
    print("Data Quality evaluation completed")

    # Extract all and passed rows
    outcomes_dyf = SelectFromCollection.apply(dq_results, key="rowLevelOutcomes")

    all_rows_dyf = sparkSqlQuery(
        glueContext, "SELECT * FROM myDataSource",
        {"myDataSource": outcomes_dyf}, "all_rows_dyf"
    )

    passed_rows_dyf = sparkSqlQuery(
        glueContext,
        "SELECT * FROM myDataSource WHERE DataQualityEvaluationResult NOT LIKE 'Failed'",
        {"myDataSource": outcomes_dyf},
        "passed_rows_dyf"
    )
    print(f"Passed rows count: {passed_rows_dyf.count()}")

    # Add metadata
    all_transformed = MyTransform(glueContext, DynamicFrameCollection({"input": all_rows_dyf}, glueContext))
    passed_transformed = MyTransform(glueContext, DynamicFrameCollection({"input": passed_rows_dyf}, glueContext))

    all_final = SelectFromCollection.apply(all_transformed, key="customTransform0")
    passed_final = SelectFromCollection.apply(passed_transformed, key="customTransform0")

    # Rename DQ result column
    renamed_final = RenameField.apply(
        frame=all_final,
        old_name="DataQualityEvaluationResult",
        new_name="result"
    )

    # Apply mapping for passed records
    # mapped_passed = ApplyMapping.apply(
    #     frame=passed_final,
    #     mappings=[
    #         ("id", "string", "id", "string"),
    #         ("smart_contract_version_id", "string", "smart_contract_version_id", "string"),
    #         ("alias", "string", "alias", "string"),
    #         ("status", "string", "status", "string"),
    #         ("source_create_timestamp", "string", "source_create_timestamp", "string"),
    #         ("source_open_timestamp", "string", "source_open_timestamp", "string"),
    #         ("global_migration_id", "string", "global_migration_id", "string"),
    #         ("parameter_values", "string", "parameter_values", "string")
    #     ]
    # )

    expected_columns = [
        "id",
        "smart_contract_version_id",
        "stakeholder_ids",
        "alias",
        "status",
        "source_create_timestamp",
        "source_open_timestamp",
        "permitted_denominations",
        "global_migration_id",
        "parameter_values"
    ]

    # Apply mapping for DQ fail records
    mapped_dq_fail = ApplyMapping.apply(
        frame=renamed_final,
        mappings=[
            ("alias", "string", "id", "string"),
            ("global_migration_id", "string", "global_migration_id", "string"),
            ("entity", "string", "entity", "string"),
            ("rules_pass", "string", "rules_pass", "string"),
            ("rules_fail", "string", "rules_fail", "string"),
            ("rules_skip", "string", "rules_skip", "string"),
            ("result", "string", "result", "string")
        ]
    )

    # Write passed records to Iceberg table
    df_account = passed_final.toDF().select(*expected_columns)
    print(f"Number of rows to write to aux_account: {df_account.count()}")
    df_account.printSchema()
    df_account.show(5, truncate=False)

    df_account.writeTo("glue_catalog.uat_migrationdb.aux_account").append()
    print("Successfully wrote to glue_catalog.uat_migrationdb.aux_account")

    # Write DQ fail records to Glue table
    print("Writing DQ fail records to dq_fails table...")
    glueContext.write_dynamic_frame.from_catalog(
        frame=mapped_dq_fail,
        database="uat_staging",
        table_name="dq_fails"
    )
    print("Successfully wrote DQ fail records to dq_fails table")

    job.commit()
    print("Glue job completed successfully.")

except Exception as e:
    print("\nJob failed with exception:")
    traceback.print_exc()
    raise
