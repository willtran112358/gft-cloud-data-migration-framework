import sys
import os
# Obtener el directorio actual del script
current_dir = os.path.dirname(__file__)
# Subir tres niveles en el directorio
library_dir = os.path.abspath(os.path.join(current_dir, '../'))
# Agregar el directorio de la biblioteca a sys.path
sys.path.append(library_dir)
import json
import uuid
from datetime import datetime, timezone
from src.kafka_conf.kafka_config import (
  get_kafka_producer,
  send_message
  )
import pandas as pd
from utils.migrationdb import (connect_to_athena,execute_athena_query)
from common.constants import RESOURCE_BATCH_PRODUCER_TOPIC
import logging
logging.basicConfig(level=logging.INFO)

BATCH_SIZE = int(os.environ.get('BATCH_SIZE','200'))
PRODUCT_VERSION_ID_TO_CHANGE_DATE = json.loads(os.environ.get('PRODUCT_VERSION_ID_TO_CHANGE_DATE','["6189","6189"]'))
ACCOUNT_PRODUCTOR_QUERY = os.environ.get('PRODUCTOR_QUERY','SELECT * FROM ACCOUNT WHERE STAKEHOLDER_IDS IN (SELECT ID FROM MASTER_CUSTOMER)') 

def format_datetime(dt):
    """Convierte un objeto datetime a una cadena en formato 'YYYY-MM-DDTHH:MM:SSZ'."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")  

  
# Function to create a Kafka message with at most 200 resources
def create_kafka_message(account_data):
  message_content = []
  num_of_c = len(account_data)
  count_batches=0
  for account in account_data:
    #TODO: Asegurar valores y formatos
    if account["smart_contract_version_id"] in PRODUCT_VERSION_ID_TO_CHANGE_DATE:
      create_ts = format_datetime(datetime.now(timezone.utc))
      open_ts = format_datetime(datetime.now(timezone.utc))
    else:
      create_date_string = account["source_create_timestamp"]
      create_dt = datetime.strptime(create_date_string, "%Y-%m-%d")
      create_ts = create_dt.strftime( "%Y-%m-%dT%H:%M:%SZ")
      open_date_string = account["source_open_timestamp"]
      open_dt = datetime.strptime(open_date_string, "%Y-%m-%d")
      open_ts = open_dt.strftime( "%Y-%m-%dT%H:%M:%SZ")
        
    message_content.append({
      "id": account["id"],
      "account_resource": {
        "account": {
          "smart_contract_version_id": account["smart_contract_version_id"],
          "stakeholder_ids": [account["stakeholder_ids"]],
          "alias": account["alias"],
          "status": account["status"],
          "source_create_timestamp": create_ts,
          "source_open_timestamp": open_ts,
          "permitted_denominations": [account["permitted_denominations"]],
          "details": {
            "global_reconciliator_id": account["details"],
            "account_opening_date": account["source_create_timestamp"],
          },
        },
      "create_options": {
        "parameter_values": json.loads(account["parameter_values"])
        }
      }
    })
    
    if len(message_content) == BATCH_SIZE or num_of_c == len(message_content):
      count_batches+=1
      message = {
        "request_id": str(uuid.uuid4()),
        "resource_batch": {
          "id": str(uuid.uuid4()),
          "resources": message_content
        }
      }
      num_of_c-=BATCH_SIZE
      yield message  # Yield the message for sending in batches
      message_content = []  # Reset the batch content for the next message
      
  print("number_of_bacthes_sent:"+str(count_batches))
  
def produce_data():
  print(f"product_version_id_to_change_date: {PRODUCT_VERSION_ID_TO_CHANGE_DATE}")
  athena_client=connect_to_athena()
  accounts = execute_athena_query(athena_client,ACCOUNT_PRODUCTOR_QUERY).to_dict(orient="records")
  # Create Kafka producer with secure connection
  producer = get_kafka_producer()

  # Send messages in batches
  for message in create_kafka_message(accounts):
    message_json = json.dumps(message)
    try:
      send_message(RESOURCE_BATCH_PRODUCER_TOPIC, message_json.encode('utf-8'), producer)
      print("OE")
    except Exception as e:
      print(f"Error sending message: {e}")

  # Close the producer connection
  producer.close()

  print(f"Messages sent to topic: {RESOURCE_BATCH_PRODUCER_TOPIC}")
  
if __name__ == "__main__":
  produce_data()
