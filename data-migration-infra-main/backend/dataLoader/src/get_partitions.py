# Obtener el directorio actual del script
import sys,os
current_dir = os.path.dirname(__file__)
# Subir tres niveles en el directorio
library_dir = os.path.abspath(os.path.join(current_dir, '../'))
# Agregar el directorio de la biblioteca a sys.path
sys.path.append(library_dir)

from confluent_kafka.admin import AdminClient

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

# def get_kafka_producer():
#     return  KafkaProducer(
#     bootstrap_servers=BOOTSTRAP_SERVER,
#     security_protocol=SECURITY_PROTOCOL,
#     sasl_mechanism=SASL_MECHANISM,
#     sasl_plain_username=SASL_USERNAME,
#     sasl_plain_password=SASL_PASSWORD,
# )
# Configuración del administrador
conf = {'bootstrap.servers': BOOTSTRAP_SERVER,
    'security.protocol': SECURITY_PROTOCOL,
    'sasl.mechanism': SASL_MECHANISM,
    'sasl.username': SASL_USERNAME,
    'sasl.password': SASL_PASSWORD}

# Crear un cliente administrador
admin_client = AdminClient(conf)

def print_partitions_for_topic(topic):
    metadata = admin_client.list_topics(topic=topic)
    if metadata.topics.get(topic) is not None:
        partitions = metadata.topics[topic].partitions
        print(f"El tema '{topic}' tiene {len(partitions)} particiones:")
       
    else:
        print(f"El tema '{topic}' no existe.")

# Nombre del tema del que deseas obtener información sobre las particiones
topic_name = "vault.data_loader_api.v1.data_loader.resource.migrated.events"

# Llamada a la función para imprimir la información de las particiones del tema
print_partitions_for_topic(topic_name)
