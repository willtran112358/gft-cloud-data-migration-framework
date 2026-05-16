import sys
import os
current_dir = os.path.dirname(__file__)
library_dir = os.path.abspath(os.path.join(current_dir, '../../../'))
sys.path.append(library_dir)
import unittest
from unittest.mock import MagicMock, patch
from src.customer_producer import create_kafka_message, produce_data

class TestKafkaFunctions(unittest.TestCase):

    def setUp(self):
        # Configurar variables simuladas para los tests
        self.customer_data = [
            {"id": 1, "status": "active", "first_name": "John", "last_name": "Doe"},
            {"id": 2, "status": "inactive", "first_name": "Jane", "last_name": "Smith"}
            # Agrega más datos de clientes según sea necesario
        ]
        self.BATCH_SIZE = 200

    def test_create_kafka_message(self):
        # Llama a la función y obtén un generador de mensajes
        message_generator = create_kafka_message(self.customer_data)

        # Verifica que los mensajes generados tengan el formato esperado
        for message in message_generator:
            self.assertIn("request_id", message)
            self.assertIn("resource_batch", message)
            self.assertIn("id", message["resource_batch"])
            self.assertIn("resources", message["resource_batch"])
            self.assertIsInstance(message["resources"], list)

            # Verifica que cada recurso tenga las claves y valores esperados
            for resource in message["resources"]:
                self.assertIn("id", resource)
                self.assertIn("customer_resource", resource)
                self.assertIn("status", resource["customer_resource"])
                self.assertIn("customer_details", resource["customer_resource"])
                self.assertIn("first_name", resource["customer_resource"]["customer_details"])
                self.assertIn("last_name", resource["customer_resource"]["customer_details"])

    @patch('src.customer_producer.connect_to_athena')
    @patch('src.customer_producer.execute_athena_query')
    @patch('src.customer_producer.get_kafka_producer')
    @patch('src.kafka_conf.kafka_config.send_message')
    def test_produce_data(self, mock_send_message, mock_get_kafka_producer, mock_execute_athena_query, mock_connect_to_athena):
        # Configura los mocks para las funciones de base de datos y Kafka
        mock_connect_to_athena.return_value = MagicMock()
        mock_execute_athena_query.return_value = MagicMock()
        mock_get_kafka_producer.return_value = MagicMock()

        # Llama a la función de producción de datos
        produce_data()

        # Verifica si se llaman a las funciones necesarias
        self.assertTrue(mock_connect_to_athena.called)
        self.assertTrue(mock_execute_athena_query.called)
        self.assertTrue(mock_get_kafka_producer.called)
        self.assertTrue(mock_send_message.called)

if __name__ == '__main__':
    unittest.main()
