import sys
import os
import time

# Obtener el directorio actual del script
current_dir = os.path.dirname(__file__)
# Subir tres niveles en el directorio
library_dir = os.path.abspath(os.path.join(current_dir, '../'))
# Agregar el directorio de la biblioteca a sys.path
sys.path.append(library_dir)
import json
import uuid
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
CUSTOMER_PRODUCTOR_QUERY = os.environ.get('PRODUCTOR_QUERY','SELECT * FROM CUSTOMER')



# Function to create a Kafka message with at most 200 resources
def create_kafka_message(customer_data):
  message_content = []
  num_of_c = len(customer_data)
  count_batches=0
  for customer in customer_data:
    
    message_content.append({
      "id": customer["id"],
      "customer_resource": {
        "status": "CUSTOMER_STATUS_ACTIVE",
        "additional_details": {
          "global_reconciliator_id": str(customer["global_migration_id"])
        }
      }
    })
    
    # Send the message if the batch reaches 200 resources or the end of data is reached
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
  athena_client=connect_to_athena()
  customers = execute_athena_query(athena_client,CUSTOMER_PRODUCTOR_QUERY).to_dict(orient="records")
  # Create Kafka producer with secure connection
  producer = get_kafka_producer()

  # Send messages in batches
  for message in create_kafka_message(customers):
    message_json = json.dumps(message)
    try:
      send_message(RESOURCE_BATCH_PRODUCER_TOPIC, message_json.encode('utf-8'), producer)
      time.sleep(1)
    except Exception as e:
      print(f"Error sending message: {e}")

  # Close the producer connection
  producer.close()

  print(f"Messages sent to topic: {RESOURCE_BATCH_PRODUCER_TOPIC}")
  
if __name__ == "__main__":
  produce_data()
