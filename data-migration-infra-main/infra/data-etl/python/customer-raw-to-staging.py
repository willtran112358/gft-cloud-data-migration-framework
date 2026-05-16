timport sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Iceberg config is already set via --conf job parameters

# Read from external raw Parquet table (S3 only, not in Glue catalog)
df = spark.read.format("parquet").load("s3://699955796816-ap-southeast-1-gft-dm-uat-raw/customer/")

# Optional: debug output
df.printSchema()
df.show(5)

# Write to Iceberg table in Glue Catalog
df.writeTo("glue_catalog.uat_staging.customer").append()

# Commit job
job.commit()
