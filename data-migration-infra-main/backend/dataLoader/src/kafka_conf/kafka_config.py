from kafka import KafkaProducer

# from common.constants import (
#   BOOTSTRAP_SERVER,
#   SECURITY_PROTOCOL,
#   SASL_MECHANISM,
#   SASL_PASSWORD,
#   SASL_USERNAME
# )

BOOTSTRAP_SERVER="b-1.mskclusterapse1ua.tgsou1.c2.kafka.ap-southeast-1.amazonaws.com:9096,b-2.mskclusterapse1ua.tgsou1.c2.kafka.ap-southeast-1.amazonaws.com:9096,b-3.mskclusterapse1ua.tgsou1.c2.kafka.ap-southeast-1.amazonaws.com:9096"
SECURITY_PROTOCOL="SASL_SSL"
SASL_MECHANISM="SCRAM-SHA-512"
SASL_USERNAME="be-data-migration"
SASL_PASSWORD="bedatamigration"

def get_kafka_producer():
    return  KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    security_protocol=SECURITY_PROTOCOL,
    sasl_mechanism=SASL_MECHANISM,
    sasl_plain_username=SASL_USERNAME,
    sasl_plain_password=SASL_PASSWORD,
)
    
# Function to send messages (replace with your message creation logic)
def send_message(topic, message, producer):
  producer.send(topic, message)
  producer.flush()  # Flush to ensure message is sent