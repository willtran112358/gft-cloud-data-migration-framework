import json
import boto3
import time
import os

athena = boto3.client('athena')
ATHENA_BUCKET = os.environ["ATHENA_BUCKET"]  
DB = os.environ["MIGRATION_DATABASE_NAME"] 


def lambda_handler(event, context):
    print(event)
    query = event['query']
    part_id = event['executionId'].split(':')
    id_execution = part_id[-1]
    print(id_execution)
    
    query_final = f"{query} where global_reconciliator_id='{id_execution}'"
    print(query_final)
    response = athena.start_query_execution(
        QueryString=query_final,
        QueryExecutionContext={'Database': DB},
        ResultConfiguration={'OutputLocation': ATHENA_BUCKET}
    )
    
    query_execution_id = response['QueryExecutionId']
    
    # Esperar a que la consulta termine
    while True:
        query_status = athena.get_query_execution(QueryExecutionId=query_execution_id)
        status = query_status['QueryExecution']['Status']['State']
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)
    
    if status == 'SUCCEEDED':
        # Obtener los resultados de la consulta
        result = athena.get_query_results(QueryExecutionId=query_execution_id)
        count = int(result['ResultSet']['Rows'][1]['Data'][0]['VarCharValue'])
        
        if count == 0:
            return {
                'statusCode': 400,
                'body': json.dumps('Count is 0')
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(f'Count is {count}')
            }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Query failed')
        }