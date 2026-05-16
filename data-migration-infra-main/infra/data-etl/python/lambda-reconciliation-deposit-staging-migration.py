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
ID_STAGING = os.environ['ID_STAGING']
ID_MIGRATION = os.environ['ID_MIGRATION']
TABLE_NAME_STAGING = os.environ['TABLE_NAME_STAGING']
TABLE_NAME_MIGRATION = os.environ['TABLE_NAME_MIGRATION']
MIGRATION_DATABASE_NAME = os.environ['MIGRATION_DATABASE_NAME']
STAGING_DATABASE_NAME = os.environ['STAGING_DATABASE_NAME']
FOLDER_PATH = os.environ['FOLDER_PATH']
LOG_DB = os.environ['LOG_DB']
LOG_TABLE = os.environ['LOG_TABLE']
STAGE = os.environ['STAGE']
ENTITY = os.environ['ENTITY']
FAILURE_RATE= os.environ['FAILURE_RATE']

# Athena configuration
athena = boto3.client('athena')

# Execute query in Athena
def execute_athena_query(query, database):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': ATHENA_BUCKET}
    )
    return response['QueryExecutionId']
    
# Check if query is finished
def is_query_finished(query_execution_id):
    response = athena.get_query_execution(QueryExecutionId=query_execution_id)
    state = response['QueryExecution']['Status']['State']
    return state in ['SUCCEEDED', 'FAILED', 'CANCELLED']

# Get paginated query results from Athena
def get_paginated_query_results(query_execution_id):
    ids = set()
    next_token = None

    while True:
        if next_token:
            response = athena.get_query_results(
                QueryExecutionId=query_execution_id,
                NextToken=next_token
            )
        else:
            response = athena.get_query_results(QueryExecutionId=query_execution_id)
        
        rows = response['ResultSet']['Rows']
        if not ids:
            rows = rows[1:]  # Skip the header only on the first page

        for row in rows:
            ids.add(row['Data'][0]['VarCharValue'])
        
        next_token = response.get('NextToken')
        if not next_token:
            break

    return ids



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

    # Queries
    query_deposit = f"SELECT {ID_STAGING} FROM {TABLE_NAME_STAGING}"
    query_account = f"SELECT {ID_MIGRATION} FROM {TABLE_NAME_MIGRATION} where smart_contract_version_id = '6189'"
    

    # Execute queries in Athena
    query_deposit_execution_id = execute_athena_query(query_deposit, STAGING_DATABASE_NAME)
    query_account_execution_id = execute_athena_query(query_account, MIGRATION_DATABASE_NAME)

    # Wait for queries to finish
    while not is_query_finished(query_deposit_execution_id) or not is_query_finished(query_account_execution_id):
        time.sleep(1)
        
    # Get results
    ids_deposit = get_paginated_query_results(query_deposit_execution_id)
    ids_account = get_paginated_query_results(query_account_execution_id)

    # Verify if all ids from deposit are in account
    missing_ids = ids_deposit - ids_account
    all_present = len(missing_ids) == 0

    # Counts
    count_ids_deposit = len(ids_deposit)
    count_ids_in_account = count_ids_deposit - len(missing_ids)

    print(f"Diff: {all_present} count deposit: {count_ids_deposit}  count account: {count_ids_in_account}")

    count_staging= count_ids_deposit
    count_migration= count_ids_in_account


    part_id = event['executionId'].split(':')
    global_migration_id = part_id[-1]
    print(f"ID: {global_migration_id}")
    
    result = count_migration / count_staging 
    
    if result >= float(FAILURE_RATE):         
        body = {
            "message": "The difference in records is acceptable",
            "recordsMigration": (count_migration),
            "recordsStaging": (count_staging)
        }
        
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        status='ok'
        records_ok=count_staging
        records_error=count_staging - count_migration
    
        insert_logs(global_migration_id, STAGE, ENTITY, status, records_ok, records_error)
        
        return response
    else:
        body = {
            "message": "The number of imported records are NOT the same",
            "recordsMigration": (count_migration),
            "recordsStaging": (count_staging)       
        }
        
        response = {
            "statusCode": 400,
            "body": json.dumps(body)
        }

        status='error'
        records_ok=count_staging
        records_error=count_staging - count_migration
    
        insert_logs(global_migration_id, STAGE, ENTITY, status, records_ok, records_error)
        
        return response
