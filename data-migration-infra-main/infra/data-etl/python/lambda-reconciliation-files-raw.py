import os
import json
import boto3
import pyarrow.parquet as pq
from io import BytesIO
from datetime import datetime

# Environment variables
REGION_NAME = os.environ['REGION_NAME']
BUCKET_NAME = os.environ['BUCKET_NAME']
ATHENA_BUCKET = os.environ['ATHENA_BUCKET']
ID = os.environ['ID']
TABLE_NAME = os.environ['TABLE_NAME']
DATABASE_NAME = os.environ['DATABASE_NAME']
FOLDER_PATH = os.environ['FOLDER_PATH']
LOG_DB = os.environ['LOG_DB']
LOG_TABLE = os.environ['LOG_TABLE']
STAGE = os.environ['STAGE']
ENTITY = os.environ['ENTITY']
FAILURE_RATE = float(os.environ['FAILURE_RATE'])


def get_dataframe_record_count(table_name: str) -> int:
    """Query Athena to count records in the specified table."""
    athena = boto3.client('athena', region_name=REGION_NAME)
    query = f"SELECT COUNT({ID}) FROM {table_name}"

    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE_NAME},
        ResultConfiguration={'OutputLocation': ATHENA_BUCKET}
    )

    query_execution_id = response['QueryExecutionId']

    # Wait for query to complete
    while True:
        status = athena.get_query_execution(QueryExecutionId=query_execution_id)
        state = status['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break

    if state == 'SUCCEEDED':
        result = athena.get_query_results(QueryExecutionId=query_execution_id)
        return int(result['ResultSet']['Rows'][1]['Data'][0]['VarCharValue'])
    else:
        raise RuntimeError(f"Athena query failed with status: {state}")


def count_csv_records(bucket: str, key: str) -> int:
    """Count the number of rows in a CSV file on S3 (excluding header)."""
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        lines = obj['Body'].read().decode('utf-8').splitlines()
        return max(len(lines) - 1, 0)  # subtract header
    except Exception as e:
        print(f"Failed to count CSV records for {key}: {e}")
        return 0


def count_parquet_records(bucket: str, key: str) -> int:
    """Count the number of rows in a Parquet file on S3."""
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        buffer = BytesIO(obj['Body'].read())
        table = pq.read_table(buffer)
        return table.num_rows
    except Exception as e:
        print(f"Failed to count Parquet records for {key}: {e}")
        return 0


def get_all_file_record_count(bucket: str, prefix: str) -> int:
    """Count all records from CSV and Parquet files in a given S3 prefix."""
    s3 = boto3.client('s3')
    total = 0

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in response.get('Contents', []):
        key = obj['Key']
        if key.endswith('.csv'):
            total += count_csv_records(bucket, key)
        elif key.endswith('.parquet'):
            total += count_parquet_records(bucket, key)

    return total


def insert_log_record(migration_id, stage, entity, status, records_ok, records_error):
    """Insert a log into the Athena logging table."""
    athena = boto3.client('athena', region_name=REGION_NAME)
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    query = (
        f"INSERT INTO {LOG_TABLE} (global_migration_id, stage, entity, status, "
        f"records_ok, records_error, execution_timestamp) "
        f"VALUES ('{migration_id}', '{stage}', '{entity}', '{status}', "
        f"'{records_ok}', '{records_error}', '{timestamp}')"
    )

    execution = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': LOG_DB},
        ResultConfiguration={'OutputLocation': ATHENA_BUCKET}
    )

    execution_id = execution['QueryExecutionId']

    while True:
        status = athena.get_query_execution(QueryExecutionId=execution_id)
        state = status['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break

    if state != 'SUCCEEDED':
        reason = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
        print(f"Failed to insert log record: {reason}")


def lambda_handler(event, context):
    """Main entry point for Lambda function."""
    try:
        global_migration_id = event['executionId'].split(':')[-1]
        print(f"Execution ID: {global_migration_id}")

        db_count = get_dataframe_record_count(TABLE_NAME)
        print(f"Athena count: {db_count}")

        file_count = get_all_file_record_count(BUCKET_NAME, FOLDER_PATH)
        print(f"S3 file count: {file_count}")

        ratio = db_count / file_count if file_count else 0
        status = 'ok' if ratio >= FAILURE_RATE else 'error'
        records_error = file_count - db_count

        insert_log_record(
            migration_id=global_migration_id,
            stage=STAGE,
            entity=ENTITY,
            status=status,
            records_ok=file_count,
            records_error=records_error
        )

        return {
            "statusCode": 200 if status == 'ok' else 400,
            "body": json.dumps({
                "message": "The difference in records is acceptable" if status == 'ok'
                           else "The number of imported records are NOT the same",
                "recordsFiles": file_count,
                "recordsRaw": db_count
            })
        }

    except Exception as e:
        print(f"Unhandled exception: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal error", "error": str(e)})
        }
