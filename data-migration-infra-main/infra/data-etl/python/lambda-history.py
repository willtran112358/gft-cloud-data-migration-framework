import boto3
import os
import time

athena = boto3.client('athena')
ATHENA_BUCKET = os.environ['ATHENA_BUCKET']  # S3 bucket to store Athena query results
S3_BUCKET_RAW = os.environ['S3_BUCKET_RAW']
S3_BUCKET_STAGING = os.environ['S3_BUCKET_STAGING']

def lambda_handler(event, context):
    database = event['database']
    table = event['table_name']
    # Check if the destination table exists
    check_query = f"SHOW TABLES LIKE '{table}_history'"
    check_result = execute_query(check_query,database)
    
    part_id = event['AWS_STEP_FUNCTIONS_STARTED_BY_EXECUTION_ID'].split(':')
    global_reconciliator_id =part_id[-1]
    print(f"ID: {global_reconciliator_id}")
    
    if not check_result['ResultSet']['Rows']:
        s3_table_creation=""
        
        if "raw" in database:
            s3_table_creation=S3_BUCKET_RAW
        else:
            s3_table_creation=S3_BUCKET_STAGING
            
        create_table_query = f"""
            CREATE TABLE {database}.{table}_history AS 
            SELECT *  FROM {database}.{table}
            WHERE 1=0
            
        """
        print (create_table_query)

        execute_query(create_table_query,database)
        
        alter_table= f"""
        ALTER TABLE {database}.{table}_history add columns (global_migration_id STRING)
        """
        execute_query(alter_table,database)
    
    # Copy data from source table to destination table
    insert_query = f"""
    INSERT INTO {database}.{table}_history
    SELECT *, '{global_reconciliator_id}' AS global_migration_id FROM {table}
    """
    execute_query(insert_query,database)
    
    return {
        'statusCode': 200,
        'body': f'Successfully copied data from {table} to {table}_history'
    }

def execute_query(query,database):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
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