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

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
# Script generated for node Custom Transform
def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    from pyspark.sql.functions import col, concat_ws
    from awsglue.utils import getResolvedOptions
    from pyspark.sql.functions import split, lit
    args = getResolvedOptions(sys.argv, ['execution_id'])
    execution_id = args['execution_id']
    last_part = execution_id.split(':')[-1] 
    df = dfc.select(list(dfc.keys())[0]).toDF()
    df = df.withColumn("entity", SqlFuncs.lit("loan")) \
        .withColumn("rules_pass", concat_ws(", ", col("DataQualityRulesPass")))\
        .withColumn("rules_fail", concat_ws(", ", col("DataQualityRulesFail")))\
        .withColumn("rules_skip", concat_ws(", ", col("DataQualityRulesSkip")))\
        .withColumn("results", concat_ws(", ", col("DataQualityEvaluationResult").cast("string")))\
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
AWSGlueDataCatalog_node1717595121542_df = glueContext.create_data_frame.from_catalog(database="development_staging", table_name="loan")
AWSGlueDataCatalog_node1717595121542 = DynamicFrame.fromDF(AWSGlueDataCatalog_node1717595121542_df, glueContext, "AWSGlueDataCatalog_node1717595121542")

# Script generated for node Drop Duplicates
DropDuplicates_node1717595159214 =  DynamicFrame.fromDF(AWSGlueDataCatalog_node1717595121542.toDF().dropDuplicates(), glueContext, "DropDuplicates_node1717595159214")

# Script generated for node SQL Query
SqlQuery1 = '''
select * from myDataSource  where account_id is not null
'''
SQLQuery_node1717595214876 = sparkSqlQuery(glueContext, query = SqlQuery1, mapping = {"myDataSource":DropDuplicates_node1717595159214}, transformation_ctx = "SQLQuery_node1717595214876")

# Script generated for node Evaluate Data Quality
EvaluateDataQuality_node1717595275716_ruleset = """
    # Example rules: Completeness "colA" between 0.4 and 0.8, ColumnCount > 10
    Rules = [
            ColumnValues "source_create_timestamp" < now(),
            ColumnValues "source_open_timestamp" < now(),
            ColumnValues "real_maturity_date" > now(),
            ColumnValues "max_maturity_date" > now(),
            ColumnValues "next_repayment_date" > now(),
            ColumnValues "denomination" matches "[a-zA-Z]*",
            ColumnLength "denomination" = 3, 
            IsComplete "stakeholder_ids",
            ColumnDataType "fec_proposed_date" = "Date",
            ColumnDataType "first_unpaid_op_date" = "Date",
            ColumnDataType "block_date" = "Date",
            ColumnDataType "original_maturity_date" = "Date",
            IsComplete "account_id"
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


# Script generated for node Custom Transform
CustomTransform_node1717596340902 = MyTransform(glueContext, DynamicFrameCollection({"SQLQuery_node1717595896664": SQLQuery_node1717595896664}, glueContext))

# Script generated for node Select From Collection
SelectFromCollection_node1717596359315 = SelectFromCollection.apply(dfc=CustomTransform_node1717596340902, key=list(CustomTransform_node1717596340902.keys())[0], transformation_ctx="SelectFromCollection_node1717596359315")

# Script generated for node Rename Field
RenameField_node1717603595183 = RenameField.apply(frame=SelectFromCollection_node1717596359315, old_name="DataQualityEvaluationResult", new_name="result", transformation_ctx="RenameField_node1717603595183")

# Script generated for node Change Schema
ChangeSchema_node1717603451970 = ApplyMapping.apply(frame=RenameField_node1717603595183, mappings=[("account_id", "string", "id", "string"), ("global_migration_id", "string", "global_migration_id", "string"), ("entity", "string", "entity", "string"), ("rules_pass", "string", "rules_pass", "string"), ("rules_fail", "string", "rules_fail", "string"), ("rules_skip", "string", "rules_skip", "string"), ("results", "string", "result", "string")], transformation_ctx="ChangeSchema_node1717603451970")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1718814758930_df = ChangeSchema_node1717603451970.toDF()
AWSGlueDataCatalog_node1718814758930 = glueContext.write_data_frame.from_catalog(frame=AWSGlueDataCatalog_node1718814758930_df, database="development_staging", table_name="dq_fails", additional_options={})

job.commit()