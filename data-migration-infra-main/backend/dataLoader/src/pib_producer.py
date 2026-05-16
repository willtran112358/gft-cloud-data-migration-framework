import sys
import os
import json
import uuid
from datetime import datetime, timezone
import logging
import pandas as pd
import pytz

logging.basicConfig(level=logging.INFO)
# As account_sequence_number is string type to order properly has to be casted
PIB_PRODUCTOR_QUERY = os.environ.get('PRODUCTOR_QUERY','SELECT * FROM POSTING_INSTRUCTION_BATCH WHERE TARGET_ACCOUNT_ID IN (SELECT ID FROM MASTER_ACCOUNT) ORDER BY CAST(account_sequence_number AS int) ASC') 



def setup_library_path():
    """Configure library path."""
    current_dir = os.path.dirname(__file__)
    library_dir = os.path.abspath(os.path.join(current_dir, '../'))
    sys.path.append(library_dir)

setup_library_path()

from src.kafka_conf.kafka_config import (get_kafka_producer, send_message)
from utils.migrationdb import (connect_to_athena,execute_athena_query)
from common.constants import PIB_PRODUCER_TOPIC

def determine_hard_settlement_type(posting):
    """Determine Hard_settlement transaction type based on credit or debit."""
    if posting["credit"].lower() == "true": 
        return "inbound_hard_settlement", str(abs(float(posting["amount"])))
    else:
        return "outbound_hard_settlement", str(abs(float(posting["amount"])))

def create_posting_instruction(posting, transaction_type, amount):
    """Create posting instruction."""
    return {
        "client_transaction_id": posting["client_transaction_id"],
        transaction_type: {
            "amount": amount,
            "denomination": posting["denomination"],
            "target_account": {
                "account_id": posting["target_account_id"],
            },
            "internal_account_id": posting["internal_account_id"],
            # "advice": posting["advice"],
        }
    }
    
def format_datetime(dt):
    """Convierte un objeto datetime a una cadena en formato 'YYYY-MM-DDTHH:MM:SSZ'."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def create_hard_settlement_message(posting):
    """Create hard settlement request."""
    #TODO: Confirmar valores y formatos de las fechas
    transaction_type, amount = determine_hard_settlement_type(posting)

    value_timestamp_string = posting["value_timestamp"]
    value_timestamp_dt = datetime.strptime(value_timestamp_string, "%Y-%m-%d")
    value_timestamp = value_timestamp_dt.strftime( "%Y-%m-%dT%H:%M:%SZ")
    
    booking_timestamp_string = posting["booking_timestamp"]
    booking_timestamp_dt = datetime.strptime(booking_timestamp_string, "%Y-%m-%d")
    booking_timestamp = booking_timestamp_dt.strftime( "%Y-%m-%dT%H:%M:%SZ")
        
    if posting["source_insert_timestamp"]:
        source_insert_timestamp_string = posting["source_insert_timestamp"]
        source_insert_timestamp_dt = datetime.strptime(source_insert_timestamp_string, "%Y-%m-%d")
        source_insert_timestamp = source_insert_timestamp_dt.strftime( "%Y-%m-%dT%H:%M:%SZ")    
    else:
        source_insert_timestamp = format_datetime(datetime.now(timezone.utc))
    # booking_timestamp = format_datetime(datetime.now(timezone.utc))
    # source_insert_timestamp = format_datetime(datetime.now(timezone.utc))
    # value_timestamp = format_datetime(datetime.now(timezone.utc))
    # booking_timestamp = source_insert_timestamp = value_timestamp = format_datetime(datetime.now(timezone.utc))

    
    return {
        "request_id": str(uuid.uuid4()),
        "posting_instruction_batch": {
            "client_id": posting["client_id"],
            "client_batch_id": posting["client_batch_id"],
            "posting_instructions": [
                create_posting_instruction(posting, transaction_type, amount)
            ],
            "batch_details": 
                json.loads(posting["batch_details"])
            ,   
            "value_timestamp": value_timestamp,
            "booking_timestamp": booking_timestamp
        },
        "source_insert_timestamp": source_insert_timestamp,
        "account_sequence_number": posting["account_sequence_number"],
        "target_account_id": posting["target_account_id"]
    }

def create_custom_instruction_message(posting):
    """Create custome_instruction request."""
    amount = str(abs(float(posting["amount"])))
    # booking_timestamp = format_datetime(datetime.now(timezone.utc))

    # booking_timestamp = format_datetime(datetime.now(timezone.utc))
    # source_insert_timestamp = format_datetime(datetime.now(timezone.utc))
    # value_timestamp = format_datetime(datetime.now(timezone.utc))
    value_timestamp_string = posting["value_timestamp"]
    value_timestamp_dt = datetime.strptime(value_timestamp_string, "%Y-%m-%d")
    value_timestamp = value_timestamp_dt.strftime( "%Y-%m-%dT%H:%M:%SZ")
    
    booking_timestamp_string = posting["booking_timestamp"]
    booking_timestamp_dt = datetime.strptime(booking_timestamp_string, "%Y-%m-%d")
    booking_timestamp = booking_timestamp_dt.strftime( "%Y-%m-%dT%H:%M:%SZ")
        
    if posting["source_insert_timestamp"]:
        source_insert_timestamp_string = posting["source_insert_timestamp"]
        source_insert_timestamp_dt = datetime.strptime(source_insert_timestamp_string, "%Y-%m-%d")
        source_insert_timestamp = source_insert_timestamp_dt.strftime( "%Y-%m-%dT%H:%M:%SZ")         
    else:
        source_insert_timestamp = format_datetime(datetime.now(timezone.utc))
        
    transaction_type = posting["transaction_type"].lower()
    
    # If the transaction is a credit means the target accoun (customer account) receives funds,
    # otherwise means the internal account is the one who earns 

    if posting["credit"].lower() == "true":
        creditor_account = posting["target_account_id"]
        creditor_account_address = posting["credit_account_address"]
        debitor_account = posting["internal_account_id"]
        debitor_account_address = posting["debit_account_address"]        
    else:
        creditor_account = posting["internal_account_id"]
        creditor_account_address = posting["debit_account_address"]
        debitor_account = posting["target_account_id"]
        debitor_account_address = posting["credit_account_address"]
    return {
        "request_id": str(uuid.uuid4()),
        "posting_instruction_batch": {
            "client_id": posting["client_id"],
            "client_batch_id": posting["client_batch_id"],
            "posting_instructions": [
                {
                    "client_transaction_id": posting["client_transaction_id"],
                    transaction_type: {
                        "postings": [
                            {
                                "credit": True,
                                "amount": amount,
                                "denomination": "EUR",
                                "account_id": creditor_account,
                                "account_address": creditor_account_address,
                                "asset": posting["asset"],
                                "phase": posting["phase"]
                            },
                            {
                                "credit": False,
                                "amount": amount,
                                "denomination": "EUR",
                                "account_id": debitor_account,
                                "account_address": debitor_account_address,
                                "asset": posting["asset"],
                                "phase": posting["phase"]
                            }
                        ],
                        "instruction_details": {
                            "description": ""
                        },
                        "override_all_restrictions": True
                    }
                }
            ],
            "batch_details": 
                json.loads(posting["batch_details"])
            ,
            "value_timestamp": value_timestamp,
            "booking_timestamp": booking_timestamp
        },
        "source_insert_timestamp": source_insert_timestamp,
        "account_sequence_number": posting["account_sequence_number"],
        "target_account_id": posting["target_account_id"]
    }
    
def create_kafka_message(posting):
    """Determine transaction type to be created, and create it."""
    if posting["transaction_type"].lower() == "hard_settlement":
        return create_hard_settlement_message(posting)
    elif posting["transaction_type"].lower() == "custom_instruction":
        return create_custom_instruction_message(posting)
    else:
        raise ValueError(f"Unsupported transaction type: {posting['transaction_type']}")

def generate_kafka_messages(pibs):
    """Generate Kafka event request."""
    for posting in pibs:
        try:
            yield create_kafka_message(posting)
        except ValueError as e:
            logging.error(f"Error creating message for posting: {e}")

def produce_data():
    """Produce data and sends messages to Kafka."""
    try:
        athena_client = connect_to_athena()
        pibs = execute_athena_query(athena_client, PIB_PRODUCTOR_QUERY).to_dict(orient="records")
    except Exception as e:
        logging.error(f"Error connecting to Athena or executing query: {e}")
        return

    producer = get_kafka_producer()

    for message in generate_kafka_messages(pibs):
        message_json = json.dumps(message)
        try:
            send_message(PIB_PRODUCER_TOPIC, message_json.encode('utf-8'), producer)
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    producer.close()
    logging.info(f"Messages sent to topic: {PIB_PRODUCER_TOPIC}")

if __name__ == "__main__":
    produce_data()
