import json
import boto3
import time
import os
from datetime import datetime
# Initialize Athena and S3 client
athena_client = boto3.client('athena')
s3_client = boto3.client('s3')


# ATHENA_BUCKET  = os.environ['ATHENA_BUCKET']
# TABLE_POLICY = os.environ['TABLE_POLICY']
# DB = os.environ['DB']
# LOG_TABLE =  os.environ['LOG_TABLE']

ATHENA_BUCKET = os.getenv('ATHENA_BUCKET', 's3://699955796816-ap-southeast-1-gft-dm-uat-athena-queries/queries-results/')
DB            = os.getenv('DB', 'uat_migrationdb')

def execute_athena_query_count(query):
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DB
        },
        ResultConfiguration={
            'OutputLocation': ATHENA_BUCKET
        }
    )
    query_execution_id = response['QueryExecutionId']
    while True:
        query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        query_state = query_status['QueryExecution']['Status']['State']
        
        if query_state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            print(query_state)
            break

        time.sleep(2)
        
    if query_state == 'SUCCEEDED':
        result_response = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        rows = result_response['ResultSet']['Rows']

        count_value = int(rows[1]['Data'][0]['VarCharValue'])
        return count_value
    else:
        raise Exception("Error executing query")
        

def compare_counts(entity,id_execution):
    
    if entity == 'customer':
        query_migration = f"SELECT COUNT(*) FROM {entity} ;"
    elif entity == 'account':
        query_migration = f"SELECT COUNT(*) FROM {entity} WHERE STAKEHOLDER_IDS IN (SELECT ID FROM master_customer);"
    else:
        query_migration = f"SELECT COUNT(*) FROM {entity} WHERE TARGET_ACCOUNT_ID IN (SELECT ID FROM master_account) ;"

    if entity == 'posting_instruction_batch':
        query_master = f"SELECT COUNT(distinct(client_batch_id)) FROM master_{entity} WHERE global_reconciliator_id='{id_execution}';"
        query_reconciliation = f"SELECT COUNT(distinct(id)) FROM reconciliation_{entity} WHERE global_reconciliator_id='{id_execution}';"
    else:    
        query_master = f"SELECT COUNT(distinct(id)) FROM master_{entity} WHERE global_reconciliator_id='{id_execution}';"
        query_reconciliation = f"SELECT COUNT(distinct(id)) FROM reconciliation_{entity} WHERE global_reconciliator_id='{id_execution}';"
        
        
    try:
        count_migration = execute_athena_query_count(query_migration)
        count_master = execute_athena_query_count(query_master)
        count_reconciliation = execute_athena_query_count(query_reconciliation)
        
        return [count_migration,count_master,count_reconciliation]
    except Exception as e:
        return []
        
def insert_logs(id_execution, stage, entity, status, records_ok, records_error):

    if entity == "posting_instruction_batch":
        entity="posting"
    # Get current timestamp
    execution_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert new record with current timestamp
    insert_query = f"INSERT INTO {LOG_TABLE} (global_migration_id, stage, entity, status, records_ok, records_error, execution_timestamp) VALUES ('{id_execution}', '{stage}', '{entity}', '{status}', '{records_ok}', '{records_error}', '{execution_timestamp}')"
    
    # Start query execution for insert
    insert_execution = athena_client.start_query_execution(
        QueryString=insert_query,
        QueryExecutionContext={'Database': DB},
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
   #event = {'executionId': 'arn:aws:states:eu-central-1:<ACCOUNTID>:execution:global-migration:45dd801a-c8a1-4128-b226-3d49ed3da532', 'entity': 'posting_instruction_batch'}
    print(event)
    entity_value = event['entity']
    part_id = event['executionId'].split(':')
    id_execution = part_id[-1]

    query = f"SELECT * FROM {TABLE_POLICY} WHERE entity = '{entity_value}' LIMIT 1;"

    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DB
        },
        ResultConfiguration={
            'OutputLocation': ATHENA_BUCKET
        }
    )
    
    query_execution_id = response['QueryExecutionId']

    while True:
        query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        query_state = query_status['QueryExecution']['Status']['State']

        if query_state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break

        time.sleep(2)

    if query_state == 'SUCCEEDED':
        result_response = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        rows = result_response['ResultSet']['Rows']
        print()
        if len(rows) > 1:  # Check if there are results (first row are the headers)
            counts= compare_counts(entity_value,id_execution)
            counts_error=int(counts[0])-int(counts[1])
            print(counts_error)
            if(counts[0]<=counts[2]):
                
                #insert logs
                if (counts[0]<=counts[1]):
                    status='ok'
                else:
                    status='error'
                    
                insert_logs(id_execution,'DATALOADER',entity_value,status,counts[0],counts_error)
                return {
                    'statusCode': 200,
                    'body': json.dumps(f'Entity exists: Migration:{counts[0]}, Master: {counts[1]}, Reconciliation: {counts[2]}')
                }
            else:
                status='error'
                
                insert_logs(id_execution,'DATALOADER',entity_value,status,counts[0],counts_error)
                return {
                    'statusCode': 404,
                    'body': json.dumps(f'Entity exists but there are fails: Migration:{counts[0]}, Master: {counts[1]}, Reconciliation: {counts[2]}')
                }
                
        else:  
        
            return {
                'statusCode': 400,
                'body': json.dumps('Entity does not exist')
            }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Error executing query')
        }
    