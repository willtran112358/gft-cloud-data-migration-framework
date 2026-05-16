# Obtener el directorio actual del script
import sys,os
current_dir = os.path.dirname(__file__)
# Subir tres niveles en el directorio
library_dir = os.path.abspath(os.path.join(current_dir, '../'))
# Agregar el directorio de la biblioteca a sys.path
sys.path.append(library_dir)

from confluent_kafka.admin import AdminClient

from common.constants import (
  BOOTSTRAP_SERVER,
  SECURITY_PROTOCOL,
  SASL_MECHANISM,
  SASL_PASSWORD,
  SASL_USERNAME
)

conf = {'bootstrap.servers': BOOTSTRAP_SERVER,
    'security.protocol': SECURITY_PROTOCOL,
    'sasl.mechanism': SASL_MECHANISM,
    'sasl.username': SASL_USERNAME,
    'sasl.password': SASL_PASSWORD}

# Crear un cliente administrador
admin_client = AdminClient(conf)

def get_partitions_for_topic(topic):
    metadata = admin_client.list_topics(topic=topic)
    if metadata.topics.get(topic) is not None:
        partitions = metadata.topics[topic].partitions
        print(f"El tema '{topic}' tiene {len(partitions)} particiones:")
        return len(partitions)
       
    else:
        print(f"El tema '{topic}' no existe.")

