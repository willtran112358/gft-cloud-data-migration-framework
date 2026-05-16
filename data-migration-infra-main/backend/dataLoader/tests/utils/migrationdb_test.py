import sys
import os
current_dir = os.path.dirname(__file__)
library_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(library_dir)
import unittest
from unittest.mock import MagicMock
from utils.migrationdb import connect_athena, execute_athena_query, execute_athena_data_operation

class TestAthenaFunctions(unittest.TestCase):

    def setUp(self):
        self.aws_access_key_id = "your_access_key_id"
        self.aws_secret_access_key = "your_secret_access_key"
        self.region_name = "your_region"
        self.database_name = "your_database_name"
        self.work_group = "your_workgroup"
        self.s3_bucket = "your_s3_bucket"

    def test_connect_athena(self):
        conn = connect_athena()
        self.assertIsNotNone(conn)

    def test_execute_athena_query(self):
        athena_client = MagicMock()
        query_string = "SELECT * FROM your_table"

        athena_client.start_query_execution.return_value = {
            'QueryExecutionId': 'test_execution_id'
        }
        athena_client.get_query_execution.side_effect = [
            {'QueryExecution': {'Status': {'State': 'RUNNING'}}},
            {'QueryExecution': {'Status': {'State': 'SUCCEEDED'}}}
        ]
        athena_client.get_query_results.return_value = {
            'ResultSet': {
                'Rows': [
                    {'Data': [{'VarCharValue': 'column1'}, {'VarCharValue': 'column2'}]},
                    {'Data': [{'VarCharValue': 'value1'}, {'VarCharValue': 'value2'}]}
                ]
            }
        }

        # Ejecutar la función y comprobar si devuelve un DataFrame
        df = execute_athena_query(athena_client, query_string)
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 1)  # Verifica si se obtiene la cantidad esperada de filas

    def test_execute_athena_data_operation(self):
        # Simula un cliente de Athena
        athena_client = MagicMock()
        query_string = "INSERT INTO your_table VALUES (value1, value2)"

        # Simula el comportamiento esperado después de la ejecución
        athena_client.start_query_execution.return_value = {
            'QueryExecutionId': 'test_execution_id'
        }
        athena_client.get_query_execution.return_value = {
            'QueryExecution': {'Status': {'State': 'SUCCEEDED'}}
        }

        # Ejecutar la función y comprobar si no hay errores
        self.assertIsNone(execute_athena_data_operation(athena_client, query_string))

if __name__ == '__main__':
    unittest.main()
