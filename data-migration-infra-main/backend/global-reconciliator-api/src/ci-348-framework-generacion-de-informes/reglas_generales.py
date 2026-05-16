"""Function to verify the General rules."""

import json
import logging
import os
import boto3
import uuid
import time
from datetime import datetime
from functools import reduce

import psutil
from utils.spark_client import SparkClient
from dotenv import load_dotenv
from google.cloud import bigquery
from google.cloud import storage
from google.cloud.exceptions import NotFound, BadRequest


from logging_config import configure_logging
from pyspark.sql import functions as F
from pyspark.sql.functions import (
    add_months,
    col,
    current_date,
    date_format,
    datediff,
    dayofmonth,
    floor,
    length,
    lit,
    lpad,
    month,
    regexp_replace,
    to_date,
    trim,
    when,
    year,
    current_timestamp,
)
from pyspark.sql.types import StringType
from pyspark.sql.window import Window


configure_logging()

ENTITY = os.environ.get('ENTITY','')

class DataProcessor:
    """Class used to modify general rules."""
    def __init__(self, sparksession="", debug: str = "N"):
        """Function that initializes the class."""
        load_dotenv()
        self.download_json_from_s3()
        self._debug = debug
        self._spark_session = sparksession
        self.ruta_json = "./src/ci-348-framework-generacion-de-informes/data/2_parametros_source.json"
        self.ruta_json_2 = "./src/ci-348-framework-generacion-de-informes/data/2_parametros_target.json"
        self.ruta_params_gen = "./src/ci-348-framework-generacion-de-informes/data/general_params.json"
        self.path = "source"
        self.path_2 = "target"
        self._uuid = uuid.uuid4()

        self.inform = self.load_json(self.ruta_json)
        self.inform_2 = self.load_json(self.ruta_json_2)
        self.data_general = self.load_json(self.ruta_params_gen)
        
    def close_spark(self):
        """Function used to close the spark session."""
        return SparkClient.close_spark(self._spark_session, "spark")

    @staticmethod
    def load_json(file_path):
        """Function used to read the .json documents that are used to load environment variables."""
        try:
            with open(file_path, encoding="utf-8") as archivo:
                return json.load(archivo)
        except Exception as e:
            logging.error("Error al cargar el archivo JSON: %s,%s", file_path, str(e))
            raise e
    
    def general_inform_parquet(self, df, nm_file):
        """
        Selects specific columns from a Spark DataFrame based on a list of column names and saves the result to a CSV file.

        :param df: Spark DataFrame to process.
        :param change_names: List of column names to select.
        :param path_output: Path of the output CSV file.
        :return: Spark DataFrame with columns selected.
        """
        self.id_report = self.inform["id_report"]
        try:
            columnas = df.columns
            for columna in columnas:
                df = df.withColumn(columna, regexp_replace(columna, "NaN", ""))
            df = df.coalesce(1)
            df.write.parquet(nm_file)
            logging.info(
                "DataFrame save %s", nm_file
            )
            return nm_file
        except Exception as e:
            logging.error("Error when selecting columns and saving the DataFrame: %s", e)
            raise
    
    def download_json_from_s3(self):

        s3 = boto3.client('s3')
        name = ['2_parametros_source.json', '2_parametros_target.json', 'general_params.json']
        bucket_name = "framework-proteccion-bucket"##Sophos
        local_dir = './src/ci-348-framework-generacion-de-informes/data'
        bucket_name = "<ACCOUNTID>-eu-central-1-gft-dm-development-migration"##GFT
        
        for n in name:
            s3_key = f'json_files/{n}'#Sophos
            s3_key = f'reconciliator-files/parameters/{ENTITY}/{n}'#GFT

            if not os.path.exists(local_dir):
                os.makedirs(local_dir)

            local_path = os.path.join(local_dir, os.path.basename(s3_key))

            s3.download_file(bucket_name, s3_key, local_path)
            
        return True

    
    def return_data_gen(self):
        """Function that returns general data for the project configuration."""
        return self.data_general