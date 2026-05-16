import sys
import os
import threading
import json
import logging
import requests
import time
# Obtener el directorio actual del script
current_dir = os.path.dirname(__file__)
# Subir tres niveles en el directorio
library_dir = os.path.abspath(os.path.join(current_dir, '../'))
# Agregar el directorio de la biblioteca a sys.path
sys.path.append(library_dir)

from concurrent.futures import ThreadPoolExecutor, as_completed
from confluent_kafka import Consumer, KafkaException,TopicPartition
from utils.get_partititons import get_partitions_for_topic
from common.constants import (
    # BOOTSTRAP_SERVER,
    # SECURITY_PROTOCOL,
    # SASL_MECHANISM,
    # SASL_PASSWORD,
    # SASL_USERNAME,
    EVENT_TYPE
)

BOOTSTRAP_SERVER="b-1.mskclusterapse1ua.tgsou1.c2.kafka.ap-southeast-1.amazonaws.com:9096,b-2.mskclusterapse1ua.tgsou1.c2.kafka.ap-southeast-1.amazonaws.com:9096,b-3.mskclusterapse1ua.tgsou1.c2.kafka.ap-southeast-1.amazonaws.com:9096"
SECURITY_PROTOCOL="SASL_SSL"
SASL_MECHANISM="SCRAM-SHA-512"
SASL_USERNAME="be-data-migration"
SASL_PASSWORD="bedatamigration"

from utils.utils import get_event_status, get_resource_type, valid_status, migration_event_filter
 
# Configuración de logging
logging.basicConfig(level=logging.INFO)
 
# Variables de entorno y configuración
HTTP_RECONCILIATOR_API = os.environ.get('HTTP_RECONCILIATOR_API','0.0.0.0:80')
# HTTP_RECONCILIATOR_API = os.environ.get('HTTP_RECONCILIATOR_API','127.0.0.1:80')
# TOPIC = os.environ.get('TOPIC','vault.data_loader_api.v1.data_loader.resource_batch.create.requests.failures')
# TOPIC = os.environ.get('TOPIC','vault.data_loader_api.v1.data_loader.resource_batch.create.responses')
TOPIC = os.environ.get('TOPIC','vault.data_loader_api.v1.data_loader.resource.migrated.events')
# TOPIC = os.environ.get('TOPIC','vault.core_api.v2.accounts.account.events')
# TOPIC = os.environ.get('TOPIC','vault.migrations.postings.requests.dlq')
# TOPIC = os.environ.get('TOPIC','vault.migrations.postings.responses')
# TOPIC = os.environ.get('TOPIC','vault.core_api.v1.balances.account_balance.events')
GROUP_ID = os.environ.get('GROUP_ID', 'consumer-group1')
 
# Contadores globales
count = 0
count2 = 0
count_lock = threading.Lock()
 
# Configuración del consumidor
consumer_config = {
        'bootstrap.servers': BOOTSTRAP_SERVER, 
        'auto.offset.reset': 'earliest',
        'security.protocol': SECURITY_PROTOCOL,
        'sasl.mechanism': SASL_MECHANISM,
        'sasl.username': SASL_USERNAME,
        'sasl.password': SASL_PASSWORD,
        'group.id': GROUP_ID,
        }
 
def process_message(msg):
    global count, count2
 
    event_data = json.loads(msg.value().decode('utf-8'))
    event_type = EVENT_TYPE[TOPIC]
    event_status = get_event_status(event_type, event_data)
    resource_type = get_resource_type(event_type, event_data)
    with count_lock:
        count += 1 
    if migration_event_filter(event_data, event_type, resource_type):
        if valid_status(event_status, event_type, resource_type):
            parameters = {
                'resource_type': resource_type,
                'event_type': event_type,
                'event_status': event_status
            }
 
            api_url = f"http://{HTTP_RECONCILIATOR_API}/validate_resource_batch/"
            headers = {"Content-Type": "application/json"}
 
            try:
                start = time.time()
                response = requests.post(api_url, json=event_data, headers=headers, params=parameters)
                end = time.time() - start
 
                if response.status_code == 200:
                    logging.info(f"Successfully sent data to FastAPI: {response.text}")
                else:
                    logging.error(f"Error sending data: {response.status_code} - {response.text}")
                with count_lock:
                    count2 += 1
 
            except requests.RequestException as e:
                logging.error(f"Error sending data to API: {e}")
 
        else:
            logging.info(f"{event_status} {resource_type} {event_type} is not sent to API")
    else:
        logging.info(f"{event_status} {resource_type} {event_type} does not belong to migration")
 
    logging.info(f"Count -> {count} Count2 -> {count2}")
 
def start_consumer(partition):
    consumer = Consumer(**consumer_config)
    # consumer.assign([{'topic': TOPIC, 'partition': partition}])
    consumer.assign([TopicPartition(TOPIC, partition)])
    logging.info(f"Consumer assigned to partition {partition}")
 
    try:
        while True:
            msg = consumer.poll(timeout=0.1)
            if msg is None:
                continue
 
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    logging.info(f"End of partition {partition}")
                else:
                    logging.error(f"Error in consumer: {msg.error()}")
                continue
 
            process_message(msg)
 
    except Exception as e:
        logging.error(f"Exception in consumer thread: {e}")
 
    finally:
        consumer.close()
        logging.info("Consumer closed")
 
if __name__ == "__main__":
    partitions = get_partitions_for_topic(TOPIC)
    with ThreadPoolExecutor(max_workers=partitions) as executor:
        futures = [executor.submit(start_consumer, i) for i in range(partitions)]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Exception in consumer execution: {e}")
 
    logging.info("All threads have finished.")
