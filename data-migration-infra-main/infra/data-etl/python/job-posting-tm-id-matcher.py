import sys
import traceback
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col, when

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

try:
    print("Starting Glue job...")

    # Load from aux_posting_instruction_batch and aux_account
    df_posting = spark.read.table("glue_catalog.uat_migrationdb.aux_posting_instruction_batch")
    df_account = spark.read.table("glue_catalog.uat_migrationdb.master_account").select("id").withColumnRenamed("id", "account_id")

    # Join posting with account (left join)
    joined_df = df_posting.join(
        df_account,
        df_posting["target_account_id"] == df_account["account_id"],
        "left"
    )

    # Add match flag
    joined_df = joined_df.withColumn(
        "matched",
        when(col("account_id").isNotNull(), True).otherwise(False)
    )

    # Split matched/unmatched
    matched_df = joined_df.filter(col("matched") == True).drop("matched", "account_id")
    unmatched_df = joined_df.filter(col("matched") == False).drop("matched", "account_id")


    print(f"Matched records: {matched_df.count()}")
    print(f"Orphaned records: {unmatched_df.count()}")


    # Clear table data
    matched_df.write \
        .format("iceberg") \
        .mode("overwrite") \
        .save("glue_catalog.uat_migrationdb.aux_posting_instruction_batch")

    unmatched_df.write \
        .format("iceberg") \
        .mode("overwrite") \
        .save("glue_catalog.uat_migrationdb.orphan_posting_instruction_batch")

    job.commit()
    print("Glue job completed successfully.")

except Exception as e:
    print("\nGlue job failed with exception:")
    traceback.print_exc()
    raise e