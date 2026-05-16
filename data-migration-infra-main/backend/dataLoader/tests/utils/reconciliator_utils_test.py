import unittest
import sys
import os
import asyncio
current_dir = os.path.dirname(__file__)
library_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(library_dir)
from backend.dataLoader.utils.reconciliator_utils import get_resource_type  

class TestGetResourceType(unittest.TestCase):

  def test_customer_resource(self):
    event_data = {"resource_batch": {"resources": "customer_resource"}}
    resource_type = get_resource_type(event_data)
    self.assertEqual(resource_type, "customer")

  def test_account_resource(self):
    event_data = {"resource_batch": {"resources": "account_resource"}}
    resource_type = get_resource_type(event_data)
    self.assertEqual(resource_type, "account")

  def test_unsupported_resource(self):
    event_data = {"resource_batch": {"resources": "other_resource"}}
    with self.assertRaises(ValueError) as error:
      get_resource_type(event_data)
    self.assertEqual(str(error.exception), "Unsupported resource type: other_resource")

  def test_missing_resource_batch(self):
    event_data = {}
    with self.assertRaises(ValueError):
      get_resource_type(event_data)

if __name__ == "__main__":
  unittest.main()
