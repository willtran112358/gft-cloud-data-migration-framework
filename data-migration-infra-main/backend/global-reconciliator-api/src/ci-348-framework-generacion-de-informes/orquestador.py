"""Orchestrator to run the reports."""
import findspark
import boto3

from reglas_generales import DataProcessor as DataProcessorReglas_Generales
from read_parquet import ReadParquet
from orquestador_aws import OrquestadorAws 
from pyspark.sql.functions import col, sum as spark_sum
import os

findspark.init()

processorGen = DataProcessorReglas_Generales("N")
path = processorGen.path

report_gft = 'AWS'
if report_gft == 'AWS':
    print("AWS")
    report = OrquestadorAws(path, 'Cloud')
    df = report.generate()

    mode = 'Cloud'
    bucket, path_final, file_prefix,key = report.return_data()
    parquet_files = []
    if mode == 'Local':
        init_dir = '/app/src/ci-348-framework-generacion-de-informes/parquetFiles'
        for root, directory, files in os.walk(init_dir):
            for file in files:
                if file.endswith('.parquet'):
                    complete_path = os.path.join(root, file)
                    parquet_files.append(complete_path)
        paths_parquet = []
        files_parquet = []
        for file in parquet_files:
            paths_parquet.append(os.path.dirname(file))
            files_parquet.append(os.path.basename(file))
    elif mode == 'Cloud':
        s3_client = boto3.client('s3')

        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=file_prefix)

        files = []
        for object in response.get('Contents', []):
            files.append(object['Key'])
        paths_parquet = []
        files_parquet = []
        for file in files:
            file = file.split('/')[-1]
            file_nm_s3 = f'{file_prefix}/{file}'

            local_path = f'/app/output_files/{file}'

            s3_client.download_file(bucket, file_nm_s3, local_path)
            paths_parquet.append('/app/output_files/')
            files_parquet.append(file)

    report = ReadParquet(paths_parquet, files_parquet, key, "AWS-report",bucket,path_final)
    df = report.compare_columns()
print("------------ DF FINAL COUNT---------------------")
print(df.count())
print(df.show(20))
print("--- Termine Bien --- :)")