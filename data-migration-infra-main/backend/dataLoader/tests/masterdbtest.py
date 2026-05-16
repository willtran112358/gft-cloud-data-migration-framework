import unittest
from unittest.mock import patch, MagicMock
from utils.masterdb import get_dataframe
import pandas as pd

class TestGetDataFrame(unittest.TestCase):
    @patch('databasetest.boto3.client')
    def test_get_dataframe_success(self, mock_boto3_client):
        mock_athena_client = MagicMock()
        mock_boto3_client.return_value = mock_athena_client

        mock_query_execution_response = {
            'QueryExecution': {
                'Status': {
                    'State': 'SUCCEEDED'
                }
            },
            'ResultSet': {
                'Rows': [
                    {'Data': [{'VarCharValue': 'Column1'}, {'VarCharValue': 'Column2'}]},
                    {'Data': [{'VarCharValue': 'Value1'}, {'VarCharValue': 'Value2'}]}
                ]
            }
        }
        mock_athena_client.start_query_execution.return_value = {'QueryExecutionId': 'test_query_execution_id'}
        mock_athena_client.get_query_execution.side_effect = [
            {'QueryExecution': {'Status': {'State': 'RUNNING'}}},
            mock_query_execution_response
        ]
        mock_athena_client.get_query_results.return_value = mock_query_execution_response

        expected_df = pd.DataFrame({'Column1': ['Value1'], 'Column2': ['Value2']})
        result_df = get_dataframe('test_table_name')

        self.assertEqual(result_df.equals(expected_df), True)

    @patch('databasetest.boto3.client')
    def test_get_dataframe_failure(self, mock_boto3_client):
        mock_athena_client = MagicMock()
        mock_boto3_client.return_value = mock_athena_client

        mock_athena_client.start_query_execution.return_value = {'QueryExecutionId': 'test_query_execution_id'}
        mock_athena_client.get_query_execution.return_value = {'QueryExecution': {'Status': {'State': 'FAILED'}}}

        result_df = get_dataframe('test_table_name')

        self.assertEqual(result_df, None)

if __name__ == '__main__':
    unittest.main()
