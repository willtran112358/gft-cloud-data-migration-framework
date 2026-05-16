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
from pyspark.sql import functions as SqlFuncs

# Script generated for node Custom Transform
def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    from awsglue.utils import getResolvedOptions
    from pyspark.sql.functions import split, lit
    args = getResolvedOptions(sys.argv, ['execution_id'])
    execution_id = args['execution_id']
    last_part = execution_id.split(':')[-1]     
    from pyspark.sql.functions import col, concat_ws
    df = dfc.select(list(dfc.keys())[0]).toDF()
    df = df.withColumn("details", SqlFuncs.lit(""))\
        .withColumn("global_migration_id", lit(last_part)) 

    # Convertir DataFrame a DynamicFrame
    dynamic_frame_transformed = DynamicFrame.fromDF(df, glueContext, "dynamic_frame_transformed")
    # Retornar la DynamicFrameCollection resultante
    return DynamicFrameCollection({"customTransform0": dynamic_frame_transformed}, glueContext)
def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
# Script generated for node Custom Transform
def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    from awsglue.utils import getResolvedOptions
    from pyspark.sql.functions import split, lit
    args = getResolvedOptions(sys.argv, ['execution_id'])
    execution_id = args['execution_id']
    last_part = execution_id.split(':')[-1]
    from pyspark.sql.functions import col, concat_ws
    df = dfc.select(list(dfc.keys())[0]).toDF()
    df = df.withColumn("entity", SqlFuncs.lit("deposit")) \
        .withColumn("rules_pass", concat_ws(", ", col("DataQualityRulesPass")))\
        .withColumn("rules_fail", concat_ws(", ", col("DataQualityRulesFail")))\
        .withColumn("rules_skip", concat_ws(", ", col("DataQualityRulesSkip")))\
        .withColumn("global_migration_id", lit(last_part))
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
AWSGlueDataCatalog_node1717595121542_df = glueContext.create_data_frame.from_catalog(database="development_staging", table_name="deposit")
AWSGlueDataCatalog_node1717595121542 = DynamicFrame.fromDF(AWSGlueDataCatalog_node1717595121542_df, glueContext, "AWSGlueDataCatalog_node1717595121542")

# Script generated for node Drop Duplicates
DropDuplicates_node1717595159214 =  DynamicFrame.fromDF(AWSGlueDataCatalog_node1717595121542.toDF().dropDuplicates(), glueContext, "DropDuplicates_node1717595159214")

# Script generated for node SQL Query
SqlQuery1 = '''
select * from myDataSource where id is not null
'''
SQLQuery_node1717595214876 = sparkSqlQuery(glueContext, query = SqlQuery1, mapping = {"myDataSource":DropDuplicates_node1717595159214}, transformation_ctx = "SQLQuery_node1717595214876")

# Script generated for node Evaluate Data Quality
EvaluateDataQuality_node1717595275716_ruleset = """
    # Example rules: Completeness "colA" between 0.4 and 0.8, ColumnCount > 10
    Rules = [
        IsComplete "id"
    ]
"""

EvaluateDataQuality_node1717595275716 = EvaluateDataQuality().process_rows(frame=SQLQuery_node1717595214876, ruleset=EvaluateDataQuality_node1717595275716_ruleset, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1717595275716", "enableDataQualityCloudWatchMetrics": True, "enableDataQualityResultsPublishing": True}, additional_options={"performanceTuning.caching":"CACHE_NOTHING"})

# Script generated for node rowLevelOutcomes
rowLevelOutcomes_node1717595353158 = SelectFromCollection.apply(dfc=EvaluateDataQuality_node1717595275716, key="rowLevelOutcomes", transformation_ctx="rowLevelOutcomes_node1717595353158")

# Script generated for node SQL Query
SqlQuery0 = '''
select *  from myDataSource 
'''
SQLQuery_node1717595896664 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":rowLevelOutcomes_node1717595353158}, transformation_ctx = "SQLQuery_node1717595896664")

# Script generated for node SQL Query
SqlQuery2 = '''
select * from myDataSource  where DataQualityEvaluationResult not like  'Failed'
'''
SQLQuery_node1717604243242 = sparkSqlQuery(glueContext, query = SqlQuery2, mapping = {"myDataSource":rowLevelOutcomes_node1717595353158}, transformation_ctx = "SQLQuery_node1717604243242")

# Script generated for node Custom Transform
CustomTransform_node1717596340902 = MyTransform(glueContext, DynamicFrameCollection({"SQLQuery_node1717595896664": SQLQuery_node1717595896664}, glueContext))

# Script generated for node Custom Transform
CustomTransform_node1717604486631 = MyTransform(glueContext, DynamicFrameCollection({"SQLQuery_node1717604243242": SQLQuery_node1717604243242}, glueContext))

# Script generated for node Select From Collection
SelectFromCollection_node1717596359315 = SelectFromCollection.apply(dfc=CustomTransform_node1717596340902, key=list(CustomTransform_node1717596340902.keys())[0], transformation_ctx="SelectFromCollection_node1717596359315")

# Script generated for node Select From Collection
SelectFromCollection_node1717604327989 = SelectFromCollection.apply(dfc=CustomTransform_node1717604486631, key=list(CustomTransform_node1717604486631.keys())[0], transformation_ctx="SelectFromCollection_node1717604327989")

# Script generated for node Rename Field
RenameField_node1717603595183 = RenameField.apply(frame=SelectFromCollection_node1717596359315, old_name="DataQualityEvaluationResult", new_name="result", transformation_ctx="RenameField_node1717603595183")

# Script generated for node Change Schema
ChangeSchema_node1717609335735 = ApplyMapping.apply(frame=SelectFromCollection_node1717604327989, mappings=[("id", "string", "id", "string"), ("product_version_id", "string", "smart_contract_version_id", "string"), ("stakeholder_ids", "string", "stakeholder_ids", "string"), ("alias", "string", "alias", "string"), ("status", "string", "status", "string"), ("start_validity_date", "string", "source_create_timestamp", "string"), ("start_date", "string", "source_open_timestamp", "string"), ("", "date", "source_close_timestamp", "string"), ("current_notional_ccy_id", "string", "permitted_denominations", "string"), ("global_migration_id", "string", "details", "string"), ("parameter_values", "string", "parameter_values", "string")], transformation_ctx="ChangeSchema_node1717609335735")

# Script generated for node Change Schema
ChangeSchema_node1717603451970 = ApplyMapping.apply(frame=RenameField_node1717603595183, mappings=[("id", "string", "id", "string"), ("global_migration_id", "string", "global_migration_id", "string"), ("entity", "string", "entity", "string"), ("rules_pass", "string", "rules_pass", "string"), ("rules_fail", "string", "rules_fail", "string"), ("rules_skip", "string", "rules_skip", "string"), ("result", "string", "result", "string")], transformation_ctx="ChangeSchema_node1717603451970")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1717609338814_df = ChangeSchema_node1717609335735.toDF()
AWSGlueDataCatalog_node1717609338814 = glueContext.write_data_frame.from_catalog(frame=AWSGlueDataCatalog_node1717609338814_df, database="development_migrationdb", table_name="aux_account", additional_options={})

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1717603455283_df = ChangeSchema_node1717603451970.toDF()
AWSGlueDataCatalog_node1717603455283 = glueContext.write_data_frame.from_catalog(frame=AWSGlueDataCatalog_node1717603455283_df, database="development_staging", table_name="dq_fails", additional_options={})

job.commit()