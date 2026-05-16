import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, array_contains, when, split

# Init
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load Iceberg tables as Spark DataFrames
customer_df = spark.read.table("glue_catalog.uat_migrationdb.customer")
aux_account_df = spark.read.table("glue_catalog.uat_migrationdb.aux_account")

# Prepare customer id column for join
cust_df = customer_df.select("id").withColumnRenamed("id", "customer_id")

# Perform array_contains join
joined_df = aux_account_df.join(
    cust_df,
    array_contains(col("stakeholder_ids"), col("customer_id")),
    "left"
)

# Add match flag
joined_df = joined_df.withColumn(
    "matched",
    when(col("customer_id").isNotNull(), True).otherwise(False)
)

# Split matched/unmatched
matched_df = joined_df.filter(col("matched") == True).drop("matched", "customer_id")
unmatched_df = joined_df.filter(col("matched") == False).drop("matched", "customer_id")

print(f"Matched records: {matched_df.count()}")
print(f"Orphaned records: {unmatched_df.count()}")

# Clear table data
matched_df.write \
    .format("iceberg") \
    .mode("overwrite") \
    .save("glue_catalog.uat_migrationdb.aux_account")

unmatched_df.write \
    .format("iceberg") \
    .mode("overwrite") \
    .save("glue_catalog.uat_migrationdb.orphan_account")


# Commit the job
job.commit()
