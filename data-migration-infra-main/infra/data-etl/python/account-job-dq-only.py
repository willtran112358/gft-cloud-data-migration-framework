import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
# Script generated for node Custom Transform
def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
        from pyspark.sql.functions import col, concat_ws
        from pyspark.sql import functions as SqlFuncs
        from awsglue.utils import getResolvedOptions
        from pyspark.sql.functions import split, lit, when
        args = getResolvedOptions(sys.argv, ['execution_id'])
        execution_id = args['execution_id']
        last_part = execution_id.split(':')[-1]
        df = dfc.select(list(dfc.keys())[0]).toDF()
        df = df.withColumn("entity", SqlFuncs.lit("account")) \
            .withColumn("rules_pass", concat_ws(", ", col("DataQualityRulesPass").cast("string"))) \
            .withColumn("rules_fail", concat_ws(", ", col("DataQualityRulesFail").cast("string"))) \
            .withColumn("rules_skip", concat_ws(", ", col("DataQualityRulesSkip").cast("string"))) \
            .withColumn("results", concat_ws(", ", col("DataQualityEvaluationResult").cast("string"))) \
            .withColumn("global_migration_id", lit(last_part))\
            .withColumn("id", when(col("id").isNull(), "EMPTY").otherwise(col("id").cast("string")))
        # Convertir DataFrame a DynamicFrame
        dynamic_frame_transformed = DynamicFrame.fromDF(df, glueContext, "dynamic_frame_transformed")
        # Retornar la DynamicFrameCollection resultante
        return DynamicFrameCollection({"customTransform0": dynamic_frame_transformed}, glueContext)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1722266405657_df = glueContext.create_data_frame.from_catalog(database="development_staging", table_name="account")
AWSGlueDataCatalog_node1722266405657 = DynamicFrame.fromDF(AWSGlueDataCatalog_node1722266405657_df, glueContext, "AWSGlueDataCatalog_node1722266405657")

# Script generated for node Evaluate Data Quality
EvaluateDataQuality_node1722266434248_ruleset = """
    # Example rules: Completeness "colA" between 0.4 and 0.8, ColumnCount > 10
    Rules = [
            IsComplete "id",
            IsComplete "product_version_id",
            IsComplete "status",
            IsComplete "stakeholder_ids"
    ]
"""

EvaluateDataQuality_node1722266434248 = EvaluateDataQuality().process_rows(frame=AWSGlueDataCatalog_node1722266405657, ruleset=EvaluateDataQuality_node1722266434248_ruleset, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1722266434248", "enableDataQualityCloudWatchMetrics": True, "enableDataQualityResultsPublishing": True}, additional_options={"performanceTuning.caching":"CACHE_NOTHING"})

# Script generated for node rowLevelOutcomes
rowLevelOutcomes_node1722266496270 = SelectFromCollection.apply(dfc=EvaluateDataQuality_node1722266434248, key="rowLevelOutcomes", transformation_ctx="rowLevelOutcomes_node1722266496270")

# Script generated for node SQL Query
SqlQuery0 = '''
select * from myDataSource
'''
SQLQuery_node1722268276820 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":rowLevelOutcomes_node1722266496270}, transformation_ctx = "SQLQuery_node1722268276820")

# Script generated for node Custom Transform
CustomTransform_node1722268613943 = MyTransform(glueContext, DynamicFrameCollection({"SQLQuery_node1722268276820": SQLQuery_node1722268276820}, glueContext))

# Script generated for node Select From Collection
SelectFromCollection_node1722268621594 = SelectFromCollection.apply(dfc=CustomTransform_node1722268613943, key=list(CustomTransform_node1722268613943.keys())[0], transformation_ctx="SelectFromCollection_node1722268621594")

# Script generated for node Change Schema
ChangeSchema_node1722271825136 = ApplyMapping.apply(frame=SelectFromCollection_node1722268621594, mappings=[("alias", "string", "id", "string"), ("global_migration_id", "string", "global_migration_id", "string"), ("entity", "string", "entity", "string"), ("rules_pass", "string", "rules_pass", "string"), ("rules_fail", "string", "rules_fail", "string"), ("rules_skip", "string", "rules_skip", "string"), ("results", "string", "result", "string")], transformation_ctx="ChangeSchema_node1722271825136")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1722271827085_df = ChangeSchema_node1722271825136.toDF()
AWSGlueDataCatalog_node1722271827085 = glueContext.write_data_frame.from_catalog(frame=AWSGlueDataCatalog_node1722271827085_df, database="development_staging", table_name="dq_fails", additional_options={})

job.commit()