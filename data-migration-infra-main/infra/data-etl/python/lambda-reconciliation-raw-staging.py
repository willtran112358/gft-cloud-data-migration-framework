import pandas as pd
import boto3
from io import BytesIO
import time
import os
import json
import re
from datetime import datetime


REGION_NAME = os.environ['REGION_NAME']
BUCKET_NAME = os.environ['BUCKET_NAME']
ATHENA_BUCKET  = os.environ['ATHENA_BUCKET']
ID_RAW = os.environ['ID_RAW']
ID_STAGING = os.environ['ID_STAGING']
TABLE_NAME_RAW = os.environ['TABLE_NAME_RAW']
TABLE_NAME_STAGING = os.environ['TABLE_NAME_STAGING']
STAGING_DATABASE_NAME = os.environ['STAGING_DATABASE_NAME']
RAW_DATABASE_NAME = os.environ['RAW_DATABASE_NAME']
LOG_DB = os.environ['LOG_DB']
LOG_TABLE = os.environ['LOG_TABLE']
STAGE = os.environ['STAGE']
ENTITY = os.environ['ENTITY']
FAILURE_RATE= os.environ['FAILURE_RATE']

def get_dataframe(table_name, db, ID):
    
    # Query data using Athena
    athena_client = boto3.client('athena',
                            region_name=REGION_NAME)
 
    # query = f"SELECT count({ID}) FROM {table_name}"
   
    query = f"SELECT count({ID}) FROM {table_name}"
    query_execution = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': db},
        ResultConfiguration={
            'OutputLocation': ATHENA_BUCKET
        }
    )
 
    # Wait for the query to finish
    query_execution_id = query_execution['QueryExecutionId']
    query_status = None
    while query_status not in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        query_execution_response = athena_client.get_query_execution(
            QueryExecutionId=query_execution_id
        )
        query_status = query_execution_response['QueryExecution']['Status']['State']
 
    # Once the query is finished, fetch the results
    if query_status == 'SUCCEEDED':
        query_results = athena_client.get_query_results(
            QueryExecutionId=query_execution_id
        )
        count = int(query_results['ResultSet']['Rows'][1]['Data'][0]['VarCharValue'])
       
        return count
       
    else:
        print("Query failed or was cancelled.")
        return None

def insert_logs(global_migration_id, stage, entity, status, records_ok, records_error):
    # Initialize Athena client
    athena_client = boto3.client('athena', region_name=REGION_NAME)
    
    # Get current timestamp
    execution_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert new record with current timestamp
    insert_query = f"INSERT INTO {LOG_TABLE} (global_migration_id, stage, entity, status, records_ok, records_error, execution_timestamp) VALUES ('{global_migration_id}', '{stage}', '{entity}', '{status}', '{records_ok}', '{records_error}', '{execution_timestamp}')"
    
    # Start query execution for insert
    insert_execution = athena_client.start_query_execution(
        QueryString=insert_query,
        QueryExecutionContext={'Database': LOG_DB},
        ResultConfiguration={'OutputLocation': ATHENA_BUCKET}
    )
    
    # Wait for the insert query to finish
    insert_execution_id = insert_execution['QueryExecutionId']
    insert_status = None
    while insert_status not in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        insert_execution_response = athena_client.get_query_execution(
            QueryExecutionId=insert_execution_id
        )
        insert_status = insert_execution_response['QueryExecution']['Status']['State']
    
    if insert_status == 'SUCCEEDED':
        print("New record inserted.")
    else:
        # Fetch error message if insert query fails
        insert_execution_status = athena_client.get_query_execution(
            QueryExecutionId=insert_execution_id
        )
        error_message = insert_execution_status['QueryExecution']['Status']['StateChangeReason']
        print(f"Error inserting new record: {error_message}")

def lambda_handler(event, context):

    
    #df_s3 = get_records_in_file()
    df_staging = get_dataframe(TABLE_NAME_STAGING, STAGING_DATABASE_NAME, ID_STAGING)
    df_raw = get_dataframe(TABLE_NAME_RAW, RAW_DATABASE_NAME, ID_RAW)

    execution_id = event['executionId']

    part_id = execution_id.split(':')[-1] if ':' in execution_id else execution_id
    global_migration_id = part_id[-1]
    print(f"ID: {global_migration_id}")
    
    result = df_staging / df_raw
    
    if result >= float(FAILURE_RATE):
        body = {
            "message": "The difference in records is acceptable",
            "recordsMigration": (df_staging),
            "recorsStagingaw": (df_raw)
        }
        
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        status='ok'
        records_ok=df_raw
        records_error=df_staging - df_raw
    
        insert_logs(global_migration_id, STAGE, ENTITY, status, records_ok, records_error)
        
        return response
    else:
        body = {
            "message": "The number of imported records are NOT the same",
            "recordsMigration": (df_staging),
            "recorsStagingaw": (df_raw)          
        }
        
        response = {
            "statusCode": 400,
            "body": json.dumps(body)
        }

        status='error'
        records_ok=df_raw
        records_error=df_staging - df_raw
    
        insert_logs(global_migration_id, STAGE, ENTITY, status, records_ok, records_error)
        
        return response
