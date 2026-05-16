"""Function to extract data and load the dataframes."""
import psutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr


class SparkClient:
    """Python class to use Spark."""

    def __init__(self):
        """Function to start the class."""
        self.spark_session = None

    def get_attributes(self):
        """Function to obtain attributes to run spark."""
        
        ram_total = psutil.virtual_memory().total

        ram_75 = ram_total * 0.75
        num_cpus = psutil.cpu_count(logical=False)

        num_cpus_75 = int(num_cpus * 0.75)

        ram_75_percent = ram_75
        num_cpus_75_percent = num_cpus_75

        return ram_75_percent, num_cpus_75_percent

    def get_spark_session(self, spark_session_name: str):
        """Function to create the spark session."""
        ram, cpu = self.get_attributes()
        ram_memory = int(ram * 0.85)
        ram_driver_memory = int(ram * 0.15)
        v_ram_memory = f"{round(ram_memory/(1024 ** 3))}g"
        v_ram_driver_memory = f"{round(ram_driver_memory/(1024 ** 3))}g"
        v_ram_memory= "1g"
        v_ram_driver_memory= "1g"
        cpu = 1
        print(
            f"These are the variables that are being used {v_ram_memory}--{v_ram_driver_memory}--- cpu----{cpu}"
        )

        if self.spark_session is None:
            spark = (
                SparkSession.builder.appName(spark_session_name)
                .config(
                    "spark.jars.packages",
                    "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.35.1",
                )
                # .config("spark.executor.memory", v_ram_memory)
                # .config("spark.driver.memory", v_ram_driver_memory)
                # .config("spark.executor.cores", cpu)
                .config("spark.memory.storageFraction", "0.8")
                .config("spark.memory.fraction", "0.8")
                .config("spark.datasource.bigquery.viewsEnabled", "true")
                .config("spark.storage.memoryFraction", "0.6")
                .getOrCreate()
                
            )
            
            spark.conf.set("spark.hadoop.fs.gs.system.bucket", "bucket-pruebas-log")

            self.spark_session = spark

            return self.spark_session

        else:
            return self.spark_session

    def close_spark(self, spark: SparkSession):
        """Function to close the spark process"""
        try:
            spark.stop()
            var = True
        except IOError as e:
            var = e
        return var

    def configure_temporary_bucket(self, spark_session: SparkSession, bucket_name: str):
        """Function to configure the GCP bucket for configuration."""
        return spark_session.conf.set("temporaryGcsBucket", bucket_name)

    def get_data_from_bigquery(
        self,
        spark_session: SparkSession,
        table_query: str,
        v_filter: str = "1=1",
        details="",
    ):
        """Function to obtain data from GCP tables."""
        DF_TABLE = (
            spark_session.read.format("bigquery")
            .option("table", table_query)
            .option("filter", v_filter)
            .load()
        )

        if "Additional_Conditions" in details:
            if details["Additional_Conditions"] != "":
                DF_TABLE = DF_TABLE.filter(expr(details["Additional_Conditions"]))

        if "Date_Column" in details:
            Start_date = details["Start_date"]
            End_date = details["End_date"]

            DF_TABLE = DF_TABLE.filter(
                (col(details["Date_Column"]) >= Start_date)
                & (col(details["Date_Column"]) <= End_date)
            )

        DF_TABLE = DF_TABLE.select(details["Campos"])

        return DF_TABLE

    def rename_df_columns(self, df, list_columns):
        """Function to rename df columns."""
        for column in list_columns:
            df = df.withColumnRenamed(column, f"{column}_del")

        return df
