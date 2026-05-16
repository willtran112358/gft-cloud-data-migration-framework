import boto3
import os
import time
from datetime import datetime

athena = boto3.client('athena')
ATHENA_BUCKET = os.environ['ATHENA_BUCKET']  # S3 bucket to store Athena query results
LOG_TABLE = os.environ['LOG_TABLE'] 
DB = os.environ['DB']
def lambda_handler(event, context):

    time_execution = event['time_execution']
    part_id = event['AWS_STEP_FUNCTIONS_STARTED_BY_EXECUTION_ID'].split(':')
    global_migration_id =part_id[-1]
    
    # Copy data from source table to destination table
    insert_query = f"""
    INSERT INTO {LOG_TABLE}
    VALUES ('{global_migration_id}','','{global_migration_id}','GLOBAL','{time_execution}','ok','','','{datetime.now()}')
    """
    execute_query(insert_query)
    
    return {
        'statusCode': 200,
        'body': f'Successfully insert data from into {LOG_TABLE}'
    }

def execute_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DB},
        ResultConfiguration={'OutputLocation': ATHENA_BUCKET}
    )
    query_execution_id = response['QueryExecutionId']
    
    # Wait for the query to complete
    status = 'RUNNING'
    while status in ['RUNNING', 'QUEUED']:
        time.sleep(5)
        status = athena.get_query_execution(QueryExecutionId=query_execution_id)['QueryExecution']['Status']['State']
    
    if status == 'SUCCEEDED':
        result = athena.get_query_results(QueryExecutionId=query_execution_id)
        return result
    else:
        raise Exception(f"Query failed with status {status}")