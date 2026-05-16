def generate_empty_reconciliation_resource_dict():
  return {
                'id': [],
                'global_reconciliator_id': [],
                'resource_batch_id': [],
                'migration_status': [],
                'migration_timestamp': [],
                'reconciliation_timestamp': []
            }  
def generate_empty_master_customer_dict():      
  return {
                'id': [],
                'status': [],
                'global_reconciliator_id' : []         
            }
  
def generate_empty_master_account_dict():      
  return {
                'id': [],
                'smart_contract_version_id': [],
                'stakeholder_ids': [],
                'alias': [],
                'status': [],
                'source_create_timestamp': [],
                'source_open_timestamp': [],
                'permitted_denominations': [],     
                'details': [],
                'processing_group_id': [],
                'parameter_values': [],
                'global_reconciliator_id' : []            
            }
  
def generate_empty_reconciliation_posting_dict():
  return {
                'id': [],
                'global_reconciliator_id': [],
                'client_batch_id': [],
                'migration_status': [],
                'migration_timestamp': [],
                'reconciliation_timestamp': []
            }   
  
def generate_empty_master_posting_dict():      
  return {
          'client_id': [],
          'client_batch_id': [],
          'client_transaction_id': [],
          'amount': [],
          'denomination': [],
          'creditor_account_id': [],
          'credit_account_address': [],
          'debit_account_address': [],
          'advice': [],
          'instruction_details': [],  
          'debitor_account_id': [],   
          'batch_details': [],
          'credit': [],
          'account_address': [],      
          'asset': [],
          'phase': [],     
          'value_timestamp': [],
          'booking_timestamp': [],
          'source_insert_timestamp': [],
          'external_transaction_id': [],
          'account_sequence_number': [],
          'global_reconciliator_id': [],
          'posting_instruction_batch_id': [],
          'target_account_id': []
          }
  
def generate_empty_master_account_balance_dict():      
  return {
          'event_id': [],
          'id': [],
          'account_id': [],
          'account_address': [],
          'phase': [],
          'asset': [],
          'denomination': [],
          'posting_instruction_batch_id': [],
          'value_time': [],
          'amount': [],  
          'total_debit': [],   
          'total_credit': [],          
          'timestamp': [],
          'related_resource_type': [],
          'related_resource_id': [],
          'sequence_number': [],  
          'migrated': []          
          }