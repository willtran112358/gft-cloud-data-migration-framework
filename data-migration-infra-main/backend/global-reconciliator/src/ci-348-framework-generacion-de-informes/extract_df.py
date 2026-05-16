"""Function used to extract and load the main dfs."""
import time
import pandas as pd
import boto3
from utils.spark_client import SparkClient
from pyspark.sql import functions as F
from pyspark.sql.types import StringType
import os
from pyspark.sql.functions import when


from reglas_generales import DataProcessor as DataProcessorReglas_Generales

SparkClient = SparkClient()

processorGen = DataProcessorReglas_Generales("N")


class ExtractDF:
    """Class used to load the main dfs."""

    def __init__(self, project_id):
        """Function that initializes the class."""
        self.project_id = project_id
        self.variable = ""
        self.change_names = ""
        self.spark = ""
        self.filter = ""
        self.general_data = processorGen.return_data_gen()

    def extract_data(self, variable, enable_join: str = "N"):
        """
        Run and process BigQuery tables.

        :param credentials: BigQuery authentication credentials.
        :param data_json: JSON object that defines the tables and fields to query.
        :return: List of pandas DataFrames with the results of the queries.
        """
        self.variable = variable
        self.change_names = variable
        self.type_source = self.variable["source"]
        self.bucket = self.variable['bucket']
        self.initial_prefix = self.variable['initial_prefix']
        spark_session = SparkClient.get_spark_session("spark-bigquery")
        self.spark = spark_session
        variable = self.variable["Tables"]["data_to_extract"].items()
        print(f"VARIABLE: {variable}")
        df_old = None
        verifidf = 0
        # Iterar a través de cada tabla especificada en el JSON de entrada
        for details in variable:
            details = details[1]
            dataframe = self.create_df(details,self.type_source)

            if self.change_names["Tables"]["Change_names"]:
                dataframe = self.raname_columns(
                    dataframe, self.change_names["Tables"]["Change_names"]
                )

            if enable_join == "Y":
                dataframe, df_old = self.is_join(df_old, details["Join"], dataframe)

        if df_old == "Y":
            dataframe = df_old
        if df_old is not None:
            verifidf = verifidf + 1
        return dataframe

    def is_join(self, df_old, join, df):
        """This Function is used when a join of the main dataframes is to be performed."""
        dataframe = df
        if self.variable["Keys"]:
            dataframe = self.cast_columns_in_dfs(dataframe, self.variable["Keys"])
        if df_old is None:
            df_old = dataframe
            df_old.repartition(100)
        else:
            for df1_columns in df_old.columns:
                if (
                    df1_columns in dataframe.columns
                    and df1_columns not in self.variable["Keys"]
                ):
                    df_old = df_old.withColumnRenamed(df1_columns, df1_columns + "_df2")
            dataframe = self.dataframe_join(
                df_old, dataframe, self.variable["Keys"], join
            )
            for column in dataframe.columns:
                if "_df2" in column:
                    dataframe = dataframe.drop(column)
            df_old = dataframe
            dataframe.repartition(100)
        return dataframe, df_old

    def raname_columns(self, dataframe, change_names):
        """
       Renames the columns of a list of DataFrames according to the given specifications.

        This function takes a list of DataFrames and renames their columns based on a predefined mapping.
        The mapping of the column names is defined in the 'informas' attribute of the instance,
        under key 'Tables' and subkey 'Name_Changes'. Only columns that exist in both
        the DataFrame as in the provided column name mapping.

        :param df_list: List of pandas DataFrames whose columns need to be renamed.

        :return: The same list of input DataFrames, but with the columns renamed according to the provided mapping.
                The renaming operation is performed in place (inplace=True), directly modifying the DataFrames
                provided in the list.

        Note: The function does not return a new set of DataFrames, but rather modifies the original DataFrames that are passed
            in the list `df_list`. This is due to the use of `inplace=True` in the `df.rename` method.
        """
        df = dataframe
        # Cargar y parsear el JSON
        Change_names = change_names
        df_columns = list(df.columns)
        # Iterar sobre cada dataframe en la lista
        for key, value in Change_names.items():
            if key in df_columns:
                df = df.withColumnRenamed(key, value)
            else:
                continue

        return df

    def cast_columns_in_dfs(self, dataframe, column_keys):
        """
        
        Cast specified columns to string in a list of DataFrames.

        :param dataframes: List of pandas DataFrames to process.
        :param json_params: JSON containing the 'Keys' key with column names to cast.
        """
        # Extraer y deduplicar los nombres de las columnas de 'Keys'
        df = dataframe
        column_names = column_keys
        columns_change = []
        # Procesar cada DataFrame
        for column in column_names:
            if column in df.columns:
                # Castear la columna a string si está presente en el DataFrame
                columns_change.append(column)
                df = df.withColumn(column, F.col(column).cast(StringType()))

        return df

    def dataframe_join(self, dataframe_one, dataframe_two, columns, how):
        """Merges multiple PySpark DataFrames into a single one, using a list of keys for the union."""
        for column in columns:
            if column in dataframe_one.columns and column in dataframe_two.columns:
                df_join = dataframe_one.join(dataframe_two, column, how)
        return df_join

    def create_df(self,details,type_source):
        """create df based on other df."""
        if type_source == 'GCP':
            
            nombre_tabla = f'{details["Project_Name"]}.{details["Set"]}.{details["Name"]}'

            if "Filter" in details:
                self.filter = details["Filter"]
            else:
                self.filter = "1=1"

            dataframe = SparkClient.get_data_from_bigquery(
                spark_session=self.spark,
                table_query=nombre_tabla,
                details=details,
                v_filter=self.filter,
            ).repartition(100)
            
            if "Limit" in details:
                dataframe = dataframe.limit(details["Limit"])
        elif type_source == 'AWS-ATHENA':

            client = boto3.client(
                    "athena",
                    region_name='eu-central-1'
            )
            s3_client = boto3.client(
                    "s3",
                    region_name='eu-central-1'
            )
            table_name = details['Name']
            fields = details['Fields']
            if len(fields) > 1:
                query = "SELECT " + ", ".join([f"{field}" for field in fields]) + f" FROM {table_name}"
            else:
                query = f"SELECT {fields[0]} FROM {table_name}"
            print(f"query: {query}")
            bucket_athena = self.general_data['athena_bucket']
            path_output = f"s3://{bucket_athena}/{self.initial_prefix}/"
            db = details['DB_Name']
            response = client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": db},
                ResultConfiguration={"OutputLocation": path_output},
            )
            query_execution_id = response["QueryExecutionId"]
            print(f"QueryExecutionId: {query_execution_id}")

            response_get_query_execution = client.get_query_execution(
                QueryExecutionId=query_execution_id
            )
            query_status = response_get_query_execution["QueryExecution"]["Status"][
                "State"
            ]
            while query_status != "SUCCEEDED":
                print(f"[102] Status: {query_status}")
                if query_status == "FAILED":
                    error = response_get_query_execution["QueryExecution"][
                        "Status"
                    ]["StateChangeReason"]
                    raise RuntimeError(f"Fail: {error}")

                response_get_query_execution = client.get_query_execution(
                    QueryExecutionId=query_execution_id
                )
                query_status = response_get_query_execution["QueryExecution"][
                    "Status"
                ]["State"]
                time.sleep(1)
            processing_key = f"{self.initial_prefix}/{query_execution_id}.csv"
            print(f"Processing key: {processing_key}")
            bucket_athena = self.general_data['athena_bucket']
            print(f"Bucket: {bucket_athena}")
            response = s3_client.get_object(Bucket=bucket_athena, Key=processing_key)
            df_pandas = pd.read_csv(response["Body"], sep=",", dtype=str, low_memory=False)
            dataframe = self.spark.createDataFrame(df_pandas)
            if 'Homologation' in details:
                for row, values in details['Homologation'].items():
                        condition = values["Condition"]
                        new_value = values["New_val"]
                        dataframe = dataframe.withColumn(row, when(dataframe[row] == condition, new_value).otherwise(dataframe[row]))
       
        return dataframe

    def return_spark_session(self):
        return self.spark
