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
    missing_ids = set()
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
        if not missing_ids:
            rows = rows[1:]  # Skip the header only on the first page

        for row in rows:
            missing_ids.add(row['Data'][0]['VarCharValue'])

        next_token = response.get('NextToken')
        if not next_token:
            break

    return missing_ids

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

    execution_id = event['executionId']

    part_id = execution_id.split(':')[-1] if ':' in execution_id else execution_id
    global_migration_id = part_id[-1]

    # Query 1: Get count from the staging table
    query_staging = f"SELECT COUNT(*) FROM {STAGING_DATABASE_NAME}.{TABLE_NAME_STAGING}"
    
    # Query 2: Get count from the migration table
    query_migration = f"SELECT COUNT(*) FROM {MIGRATION_DATABASE_NAME}.{TABLE_NAME_MIGRATION}"
    
    # Query 3: Get missing IDs from the staging table that don't exist in the migration table
    query_mismatch = f"""
    SELECT t1.{ID_STAGING}
    FROM {STAGING_DATABASE_NAME}.{TABLE_NAME_STAGING} AS t1
    LEFT JOIN {MIGRATION_DATABASE_NAME}.{TABLE_NAME_MIGRATION} AS t2
    ON t1.{ID_STAGING} = t2.{ID_MIGRATION}
    WHERE t2.{ID_MIGRATION} IS NULL
    """
    
    # Execute the three queries in sequence and wait for the results
    query_staging_execution_id = execute_athena_query(query_staging, STAGING_DATABASE_NAME)
    query_migration_execution_id = execute_athena_query(query_migration, MIGRATION_DATABASE_NAME)
    query_mismatch_execution_id = execute_athena_query(query_mismatch, STAGING_DATABASE_NAME)
    
    # Wait for all queries to finish
    while not (is_query_finished(query_staging_execution_id) and 
               is_query_finished(query_migration_execution_id) and 
               is_query_finished(query_mismatch_execution_id)):
        time.sleep(1)
    
    # Get counts from query results
    count_staging = get_paginated_query_results(query_staging_execution_id).pop()
    count_migration = get_paginated_query_results(query_migration_execution_id).pop()
    missing_ids = get_paginated_query_results(query_mismatch_execution_id)
    
    # Convert the results to integers (first element of the row is the count)
    count_staging = int(count_staging)
    count_migration = int(count_migration)
    count_missing = len(missing_ids)

    print(f"Staging count: {count_staging}")
    print(f"Migration count: {count_migration}")
    print(f"Missing IDs count: {count_missing}")

    # Avoid division by zero and handle missing records
    if count_staging == 0:
        body = {
            "message": "No records found in the staging table.",
            "recordsMigration": 0,
            "recordsStaging": 0
        }
        response = {
            "statusCode": 400,
            "body": json.dumps(body)
        }

        status = 'error'
        records_ok = 0
        records_error = 0

        insert_logs(global_migration_id, STAGE, ENTITY, status, records_ok, records_error)
        
        return response

    # Calculate the result ratio
    count_migration = count_staging - count_missing  # All present if count_missing == 0
    result = 0 if count_staging == 0 else count_migration / count_staging

    if result >= float(FAILURE_RATE):
        body = {
            "message": "The difference in records is acceptable",
            "recordsMigration": count_migration,
            "recordsStaging": count_staging
        }
        
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        status = 'ok'
        records_ok = count_staging
        records_error = count_staging - count_migration
    
        insert_logs(global_migration_id, STAGE, ENTITY, status, records_ok, records_error)
        
        return response
    else:
        body = {
            "message": "The number of imported records are NOT the same",
            "recordsMigration": count_migration,
            "recordsStaging": count_staging       
        }
        
        response = {
            "statusCode": 400,
            "body": json.dumps(body)
        }

        status = 'error'
        records_ok = count_staging
        records_error = count_staging - count_migration
    
        insert_logs(global_migration_id, STAGE, ENTITY, status, records_ok, records_error)
        
        return response

