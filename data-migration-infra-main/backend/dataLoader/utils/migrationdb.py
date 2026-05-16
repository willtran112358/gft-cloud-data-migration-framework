import sys
import os
current_dir = os.path.dirname(__file__)
library_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(library_dir)
import boto3
import pandas as pd
import logging
from common.constants import (
  AWS_ACCESS_KEY_ID,
  AWS_SECRET_ACCESS_KEY,
)

WORKGROUP="primary"
REGION_NAME="ap-southeast-1"
DATABASE_NAME="uat_migrationdb"
S3_BUCKET="s3://699955796816-ap-southeast-1-gft-dm-uat-athena-queries/queries-results/"

import awswrangler as wr
from pyathena import connect

def connect_athena():
    conn = connect(s3_staging_dir=S3_BUCKET,
                region_name=REGION_NAME,
                cursor_fetch_size=1,
                work_group=WORKGROUP,
                # aws_access_key_id=AWS_ACCESS_KEY_ID,
                # aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                # schema_name=DATABASE_NAME
                )
    return conn
 
def insert_data(data_dict,table_name,session,temp_table):
# Configuración de la conexión con Athena
    df=pd.DataFrame(data_dict)

    wr.athena.to_iceberg(
    df=df,
    database=DATABASE_NAME,
    table=table_name,
    temp_path=f"s3://699955796816-ap-southeast-1-gft-dm-uat-migration/{temp_table}/",
    keep_files=False,
    schema_evolution=True,
    boto3_session=session
)
    
    
    logging.info(f"dataframe inserted correctly in athena, table: {table_name}")
    
    
def connect_to_athena():
    """
    Establishes a connection to the Athena service using the provided credentials and region.

    Args:
        aws_access_key_id (str): The AWS access key ID.
        aws_secret_access_key (str): The AWS secret access key.
        region_name (str): The AWS region where the Athena service is located.

    Returns:
        boto3.client: The Athena client object.
    """

    athena_client = boto3.client('athena', region_name=REGION_NAME)
    
    return athena_client



def execute_athena_query(athena_client, query_string):
    """
    Executes a SQL query on the specified Athena table and waits for completion.

    Args:
        athena_client (boto3.client): The Athena client object.
        database_name (str): The name of the Athena database containing the table.
        table_name (str): The name of the Athena table to query.
        query_string (str): The SQL query to execute.

    Returns:
        None: Returns None after the query execution and result retrieval.
    """

    # Ejecuta la consulta de inserción
    query_execution = athena_client.start_query_execution(
        QueryString=query_string,
        QueryExecutionContext={'Database': DATABASE_NAME},
        ResultConfiguration={
            'OutputLocation': S3_BUCKET
        }
    )

    # Espera a que la consulta finalice
    query_execution_id = query_execution['QueryExecutionId']
    query_status = None
    while query_status not in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        query_execution_response = athena_client.get_query_execution(
            QueryExecutionId=query_execution_id
        )
        query_status = query_execution_response['QueryExecution']['Status']['State']
    
    all_results = []

    # Variable para almacenar el token de paginación
    next_token = None

# Once the query is finished, fetch the results
    if query_status == 'SUCCEEDED':
        print("succeded")
        while True:
            if next_token is None:
                query_results = athena_client.get_query_results(QueryExecutionId=query_execution_id)
            else:
                query_results = athena_client.get_query_results(QueryExecutionId=query_execution_id, NextToken=next_token)

            all_results.extend(query_results['ResultSet']['Rows'])
            

            # Verifica si hay más resultados disponibles
            if 'NextToken' in query_results:
                next_token = query_results['NextToken']
            else:
                break
        print(len(all_results))
        print(all_results[0])
            # Convert the results to a pandas DataFrame
        columns = [col['VarCharValue'] for col in all_results[0]['Data']]
            
            # Initialize an empty list to store data rows
        data_rows = []
            
            # Iterate over the result sets and append data rows
        for row in all_results[1:]:
            data_rows.append([field.get('VarCharValue', None) for field in row['Data']])
        
        # Displaying the DataFrame
        df = pd.DataFrame(data_rows,columns=columns)
        
        print(df)
        
        return df
        
    else:
        print("Query failed or was cancelled.")
        
        return None

def execute_athena_data_operation(athena_client, query_string):
    """
    Executes an Athena query using the provided query string and optional.

    Args:
        athena_client (boto3.client): The Athena client object.
        query_string (str): The base Athena query string.

    Returns:
        None: Returns None after the query execution.
    """

    query_execution = athena_client.start_query_execution(
        QueryString=query_string,
        QueryExecutionContext={'Database': DATABASE_NAME},
        ResultConfiguration={
            'OutputLocation': S3_BUCKET  # Ubicación de resultados en S3
        }
    )

    # Espera a que la consulta finalice
    query_execution_id = query_execution['QueryExecutionId']
    query_status = None
    while query_status not in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        query_execution_response = athena_client.get_query_execution(
            QueryExecutionId=query_execution_id
        )
        query_status = query_execution_response['QueryExecution']['Status']['State']

    # Verifica el estado de la consulta
    if query_status == 'SUCCEEDED':
        print("Datos insertados correctamente en la tabla.")
    else:
        print(f"Error al insertar datos: {query_status}")
        raise Exception

    return None

if __name__ == "__main__":
    athena_client=connect_to_athena()
    execute_athena_query(athena_client, "select * from customer")