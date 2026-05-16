"""Orchestrator to execute the process."""
from datetime import datetime
import boto3
import os
import findspark
from extract_df import ExtractDF
from reglas_generales import DataProcessor as DataProcessorReglas_Generales
from pyspark.sql.functions import col, sum as spark_sum

findspark.init()

processorGen = DataProcessorReglas_Generales("N")
extract = ExtractDF("AWS-Project")

class OrquestadorAws:

    def __init__(self, path: str = "parquet", location: str = "Local"):
        self.path = path
        self.location = location
       
    def generate(self):
        """Function that executes the ETL."""
        informs = []
        informs.append(processorGen.inform)
        informs.append(processorGen.inform_2)
        paths = []
        paths.append(processorGen.path)
        paths.append(processorGen.path_2)
        i = 0
        print(F"INFORMS:{informs}")
        for inform in informs:
            path = paths[i]
            self.path_final = inform['path_final']
            self.files_prefix = inform['files_prefix']
            self.key = inform['parquet_key']
            variables = inform["Tables"]["data_to_extract"].items()
            print(F"VARIABLES----:{variables}")
            n_tables = len(variables)
            if n_tables > 1 :
                join = "Y"
            else:
                join = "N"
            df_data = extract.extract_data(
                inform, join
            ).repartition(100)
            df_data.cache()
            df_data = df_data.distinct()
            print(f"DF:{df_data}")
            processorGen.general_inform_parquet(
                df_data, f"/app/output_files/{path}"
            )

            if self.location == "Cloud":
                s3_client = boto3.client('s3')
                directory = f"/app/output_files/{path}"
                files = os.listdir(directory)
                nm_files = ""
                for file in files:
                    if file.endswith('.parquet'):
                        nm_files = file
                file_local = f"/app/output_files/{path}/{nm_files}"
                bucket_name = inform["bucket"]
                self.bucket = bucket_name
                nm_file_s3 = f'{inform["files_prefix"]}/{path}.parquet'
                s3_client.upload_file(file_local, bucket_name, nm_file_s3)
            i = i + 1
        return df_data
    
    def return_data(self):
        return self.bucket, self.path_final, self.files_prefix, self.key
