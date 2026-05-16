import awswrangler as wr
import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, concat, lit, round, concat_ws, collect_list
from operator import add
from functools import reduce
import boto3

from utils.spark_client import SparkClient
from reglas_generales import DataProcessor as DataProcessorReglas_Generales

SparkClient = SparkClient()

processorGen = DataProcessorReglas_Generales("N")
print(f"ProcessorG: {processorGen}")
class ReadParquet:
    def __init__(self, paths_parquet, files_parquet, key_column, report_id, bucket, path_file):
        self.files_parquet = files_parquet
        self.paths_parquet = paths_parquet
        self.key_column = key_column
        self.report_id = report_id
        self.bucket = bucket
        self.path_final = path_file
        self.nm_final_file = processorGen.return_data_gen()
        self.nm_final_file = self.nm_final_file['final_table_name']
        POSTGRES_USER="-"
        POSTGRES_PASSWORD="-"
        POSTGRES_PORT=5432
        POSTGRES_DB="-"
        POSTGRES_SERVER="-"

        CONNECTION = f"jdbc:postgresql://{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

        db_url = CONNECTION
        self.db_url = CONNECTION
        db_properties =  {
            "user": POSTGRES_USER,
            "password": POSTGRES_PASSWORD,
            "driver": "org.postgresql.Driver"
        }
        
        self.db_properties = db_properties

        spark = SparkSession.builder \
            .appName("columns comparation by key") \
            .config("spark.jars", "/app/postgresql-42.2.24.jar") \
            .getOrCreate()
        self.spark_session = spark
        self.df1 = spark.read.parquet(f'{self.paths_parquet[0]}/{self.files_parquet[0]}')
        self.df2 = spark.read.parquet(f'{self.paths_parquet[1]}/{self.files_parquet[1]}')

    def compare_columns(self):
        df1 = self.df1
        df2 = self.df2
        key_column = self.key_column
        report_id = self.report_id

        columns_df1 = [column for column in df1.columns if column != key_column]
        columns_df2 = [column for column in df2.columns if column != key_column]
        
        origin_fields = [concat(lit(f"{c}:"), col(c)) for c in columns_df1]
        df1 = df1.withColumn("OriginField", concat_ws("|", *origin_fields))
        #df1 = df1.withColumn("OriginField", concat_ws("|", *columns_df1))

        target_fields = [concat(lit(f"{c}:"), col(c)) for c in columns_df2]
        df2 = df2.withColumn("targetField", concat_ws("|", *target_fields))
        #df2 = df2.withColumn("targetField", concat_ws("|", *columns_df2))
        
   
        joined_df = df1.alias("left").join(df2.alias("right"), on=key_column, how='inner')
        

        joined_df = joined_df.withColumn("key", col(key_column))
        

        for column_df1 in columns_df1:
            if column_df1 in df2.columns:
                joined_df = joined_df.withColumn(column_df1 + "_compare", 
                    when(col("left." + column_df1) == col("right." + column_df1), 1)
                    .otherwise(0))
                joined_df = joined_df.withColumn(column_df1 + "_equal", 
                    when(col("left." + column_df1) == col("right." + column_df1), " ")
                    .otherwise(concat(lit(column_df1), lit(": Origen -> "), col("left." + column_df1), lit(", Destino -> "), col("right." + column_df1))))
        
        columns_equal = [column for column in joined_df.columns if "_equal" in column]
        detail_columns = [concat(lit(f"{c.replace('_equal', '')}: "), col(c)) for c in columns_equal]
        joined_df = joined_df.withColumn("detailError", concat_ws("|", *detail_columns))
        #joined_df = joined_df.withColumn("detailError", concat_ws("|", *columns_equal))
        columns_to_sum = [col(column) for column in joined_df.columns if "_compare" in column]
        if columns_to_sum:
            total_comparison = reduce(add, columns_to_sum)
        else:
            total_comparison = lit(0)
        joined_df = joined_df.withColumn("result", round(total_comparison * 100  / len(columns_df1), 2))
        
        joined_df = joined_df.withColumn("r_report_id", lit(report_id))
        
        for column in joined_df.columns:
            if "_compare" in column or "_equal" in column:
                joined_df = joined_df.drop(column)
        mode = 'ATHENA-AWS'
        joined_df = joined_df.select("key","OriginField","targetField", "result","detailError","r_report_id")
        
        if mode == 'Postgres':
            
            joined_df.write \
                .jdbc(url=self.db_url, table="public.reconciliation_reports", mode="overwrite", properties=self.db_properties)
        elif mode == 'ATHENA-AWS':
            s3_client = boto3.client('s3')
            processorGen.general_inform_parquet(
                joined_df, f"/app/output_files/final/"
            )
            directory = f"/app/output_files/final/"
            files = os.listdir(directory)
            nm_file = ""
            for file in files:
                if file.endswith('.parquet'):
                    nm_file = file
            file_local = f"/app/output_files/final/{nm_file}"
            bucket_name = self.bucket
            nm_file_s3 = f'{self.path_final}/{self.nm_final_file}'

            s3_client.upload_file(file_local, bucket_name, nm_file_s3)

        return joined_df