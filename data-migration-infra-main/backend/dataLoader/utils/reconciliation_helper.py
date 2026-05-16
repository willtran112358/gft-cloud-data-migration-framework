from datetime import datetime,timedelta
from utils.migrationdb import insert_data   
import json 
import logging
def compare_time(time,sequence_time):
    now=datetime.now()
    difference= now - sequence_time
    print(difference)
    if difference >= timedelta(seconds=time):
        print("se ejecuta el insert")
        return True
    else:
        print("no se ejecuta el insert")
        return False
    
def insert_data_dict(sesion,data,temp_name,table_name):
    insert_data(data,table_name,sesion,temp_name)
    
def handle_customer_loaded(event_data,customer_reconciliator_data,customer_master_data):
    update_status = event_data["resource_migrated"]["vault_resource_loaded"]["resource_status"]

    update_timestamp = event_data.get("timestamp")   
    # Remove extra microseconds
    original_date_time_without_microseconds = update_timestamp[:23] + update_timestamp[-1]
    migration_timestamp = datetime.strptime(original_date_time_without_microseconds, "%Y-%m-%dT%H:%M:%S.%fZ")
    customer_id = event_data["resource_migrated"]["vault_resource_loaded"].get("id")
    status_message = event_data["resource_migrated"]["vault_resource_loaded"].get("status_message")
    status=f"{update_status} {status_message}"
    resource_batch_id = event_data["resource_migrated"]["vault_resource_loaded"].get("resource_batch_id")
    customer_status = event_data["resource_migrated"]["vault_resource_loaded"]['customer_resource'].get('status')
    global_reconciliator_id=event_data.get("resource_migrated", {}).get("vault_resource_loaded", {}).get("customer_resource", {}).get("additional_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT")  
    
    try:
        customer_reconciliator_data['id']+=[customer_id]
        customer_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
        customer_reconciliator_data['resource_batch_id']+=[resource_batch_id]
        customer_reconciliator_data['migration_status']+=[status]
        customer_reconciliator_data['migration_timestamp']+=[migration_timestamp]
        customer_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]
        
        customer_master_data['id']+=[customer_id]
        customer_master_data['status']+=[customer_status]
        customer_master_data['global_reconciliator_id']+=[global_reconciliator_id]
                        
        # print(customer_reconciliator_data)
        


    except Exception as e:
        # Error handling
        print(f"Error during update or copy: {e}")

def handle_resource_failed(event_data,resource_type,customer_reconciliator_data,account_reconciliator_data):
    resource_type_lower = resource_type.lower()  # Conversion due resource_type within json is lowercase
    update_status = event_data["resource_migrated"]["vault_resource_loaded"]["resource_status"]
    status_message = event_data["resource_migrated"]["vault_resource_loaded"].get("status_message")
    status=f"{update_status}: {status_message}"
    update_timestamp = event_data.get("timestamp")
    # Remove extra microseconds
    original_date_time_without_microseconds = update_timestamp[:23] + update_timestamp[-1]
    migration_timestamp = datetime.strptime(original_date_time_without_microseconds, "%Y-%m-%dT%H:%M:%S.%fZ")
    resource_id = event_data["resource_migrated"]["vault_resource_loaded"].get("id")
    resource_batch_id = event_data["resource_migrated"]["vault_resource_loaded"].get("resource_batch_id")
    #global_reconciliator_id=event_data.get("resource_migrated", {}).get("resource", {}).get(resource_type_lower, {}).get("additional_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 
    #Si no se hace esto no se agregar el global_reconciliator_id en las tablas de account
    if resource_type ==  "CUSTOMER_RESOURCE":
        global_reconciliator_id=event_data.get("resource_migrated", {}).get("vault_resource_loaded", {}).get(resource_type_lower, {}).get("additional_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 
    elif resource_type ==  "ACCOUNT_RESOURCE":
        global_reconciliator_id=event_data.get("resource_migrated", {}).get("vault_resource_loaded", {}).get(resource_type_lower, {}).get("account", {}).get("details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 

    try:
        if resource_type ==  "CUSTOMER_RESOURCE":
            customer_reconciliator_data['id']+=[resource_id]
            customer_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
            customer_reconciliator_data['resource_batch_id']+=[resource_batch_id]
            customer_reconciliator_data['migration_status']+=[status]
            customer_reconciliator_data['migration_timestamp']+=[migration_timestamp]
            customer_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]
            # print(customer_reconciliator_data)    
            
        elif resource_type ==  "ACCOUNT_RESOURCE":
            account_reconciliator_data['id']+=[resource_id]
            account_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
            account_reconciliator_data['resource_batch_id']+=[resource_batch_id]
            account_reconciliator_data['migration_status']+=[status]
            account_reconciliator_data['migration_timestamp']+=[migration_timestamp]
            account_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]                
            # print(account_reconciliator_data)
            
    except Exception as e:
        # Error handling
        print(f"Error during update or copy: {e}")
        
def handle_resource_duplicated(event_data,resource_type,customer_reconciliator_data,account_reconciliator_data):
    resource_type_lower = resource_type.lower()
    resource_batch_id=event_data.get('id')
    update_status=event_data.get('status')
    update_timestamp=event_data.get('last_updated_timestamp')
    # Remove extra microseconds
    original_date_time_without_microseconds = update_timestamp[:23] + update_timestamp[-1]
    migration_timestamp = datetime.strptime(original_date_time_without_microseconds, "%Y-%m-%dT%H:%M:%S.%fZ")
    update_validation_error=event_data.get('validation_error')
    status=f"{update_status}: at least one {update_validation_error}"
    resource_ids = []   
    try:
        for resource in event_data['resources']:
            print(resource)
            resource_id = resource.get('id')
            #global_reconciliator_id=resource.get(resource_type_lower, {}).get("additional_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT")
            # midificacion porque en duplicados no agrega el global_reconciliator_id para las account
            if resource_type ==  "CUSTOMER_RESOURCE":
                global_reconciliator_id=resource.get(resource_type_lower, {}).get("additional_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 
            elif resource_type ==  "ACCOUNT_RESOURCE":
                global_reconciliator_id=resource.get(resource_type_lower, {}).get("account", {}).get("details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 

            if resource_id:
                resource_ids.append(resource_id)
            
                if resource_type ==  "CUSTOMER_RESOURCE":
                    customer_reconciliator_data['id']+=[resource_id]
                    customer_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
                    customer_reconciliator_data['resource_batch_id']+=[resource_batch_id]
                    customer_reconciliator_data['migration_status']+=[status]
                    customer_reconciliator_data['migration_timestamp']+=[migration_timestamp]
                    customer_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]
                    # print(customer_reconciliator_data)    
                elif resource_type ==  "ACCOUNT_RESOURCE":
                    account_reconciliator_data['id']+=[resource_id]
                    account_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
                    account_reconciliator_data['resource_batch_id']+=[resource_batch_id]
                    account_reconciliator_data['migration_status']+=[status]
                    account_reconciliator_data['migration_timestamp']+=[migration_timestamp]
                    account_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]                
                    # print(account_reconciliator_data)
        

    except Exception as e:
        # Error handling
        print(f"Error during update or copy: {e}")
            
def handle_account_updated(event_data,account_reconciliator_data,account_master_data):
    account_id = event_data["account_updated"]["account"]["id"]
    smart_contract_version_id = event_data["account_updated"]["account"]["smart_contract_version_id"]
    stakeholder_ids = event_data["account_updated"]["account"]["stakeholder_ids"]
    alias = event_data["account_updated"]["account"]["alias"]
    status = event_data["account_updated"]["account"]["status"]
    source_create_timestamp = event_data["account_updated"]["account"]["source_create_timestamp"]
    source_open_timestamp = event_data["account_updated"]["account"]["source_open_timestamp"]
    permitted_denominations = event_data["account_updated"]["account"]["permitted_denominations"]
    details = event_data["account_updated"]["account"]["details"]
    processing_group_id = event_data["account_updated"]["account"]["processing_group_id"]
    parameter_values = "" # Parameters are not present in response event vault.core_api.v2.accounts.account.events        
    global_reconciliator_id=event_data.get("account_updated", {}).get("account", {}).get("details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 
    update_timestamp = event_data.get("timestamp")   
    # Remove extra microseconds
    original_date_time_without_microseconds = update_timestamp[:23] + update_timestamp[-1]
    migration_timestamp = datetime.strptime(original_date_time_without_microseconds, "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        account_reconciliator_data['id']+=[account_id]
        account_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
        account_reconciliator_data['resource_batch_id']+=["there is not resource_batch_id in event vault.core_api.v2.accounts.account.events"] #[resource_batch_id]
        account_reconciliator_data['migration_status']+=[status]
        account_reconciliator_data['migration_timestamp']+=[migration_timestamp]
        account_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]
        # print(f"reconciliator_data: {account_reconciliator_data}")
        
        account_master_data['id']+=[account_id]
        account_master_data['smart_contract_version_id']+=[smart_contract_version_id]
        account_master_data['stakeholder_ids']+=stakeholder_ids
        account_master_data['alias']+=[alias]
        account_master_data['status']+=[status]
        account_master_data['source_create_timestamp']+=[source_create_timestamp]
        account_master_data['source_open_timestamp']+=[source_open_timestamp]
        account_master_data['permitted_denominations']+=permitted_denominations
        account_master_data['details']+=[str(details)]
        account_master_data['processing_group_id']+=[processing_group_id]
        account_master_data['parameter_values']+=[parameter_values]
        account_master_data['global_reconciliator_id']+=[global_reconciliator_id]
        # print(f"account_master_data: {account_master_data}")
                                        
    except Exception as e:
        print(f"Error during update or copy: {e}")          
        
def handle_dlq_resources(event_data,customer_reconciliator_data,account_reconciliator_data,resource_type):
    resource_type_lower = resource_type.lower()  # Conversion due resource_type within json is lowercase
    resource_batch_id = event_data["resource_batch"].get("id")
    status = "DLQ: wrong request format or invalid enum values at least in one resource within the batch"
    try:
        for resource in event_data["resource_batch"]["resources"]:       
            #global_reconciliator_id=resource.get(resource_type_lower, {}).get("additional_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 
            resource_id = resource.get('id')
            #Si no se hace esto no se agregar el global_reconciliator_id en las tablas de account
            if resource_type ==  "CUSTOMER_RESOURCE":
                global_reconciliator_id=resource.get(resource_type_lower, {}).get("additional_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 
            elif resource_type ==  "ACCOUNT_RESOURCE":
                global_reconciliator_id=resource.get(resource_type_lower, {}).get("account", {}).get("details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 
            #DLQ doesn't provide error info, contains the same request posted without extra info
            # print(len(customer_reconciliator_data))
            
            if resource_type ==  "CUSTOMER_RESOURCE":
                customer_reconciliator_data['id']+=[resource_id]
                customer_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
                customer_reconciliator_data['resource_batch_id']+=[resource_batch_id]
                customer_reconciliator_data['migration_status']+=[status]
                customer_reconciliator_data['migration_timestamp']+=[datetime.now()]
                customer_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]
                # print(customer_reconciliator_data)    
            elif resource_type ==  "ACCOUNT_RESOURCE":
                account_reconciliator_data['id']+=[resource_id]
                account_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
                account_reconciliator_data['resource_batch_id']+=[resource_batch_id]
                account_reconciliator_data['migration_status']+=[status]
                account_reconciliator_data['migration_timestamp']+=[datetime.now()]
                account_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]                
                # print(account_reconciliator_data)
        
            # print(customer_reconciliator_data)
    except Exception as e:
        print(f"Error during update or copy: {e}")
            
def handle_migrated_postings(event_data,posting_reconciliator_data,posting_master_data):
    #TODO: account_sequence_number and credit are not in vault.api.v1.postings.posting_instruction_batch.created, think about use 
    #vault.migrations.postings.responses instead
    target_account_id = ""
    advice = ""
    credit = ""
    internal_account_id = ""
    credit_account_address = ""
    debit_account_address = ""
    
    client_transaction_id=event_data["posting_instruction_batch"]["posting_instructions"][0]["client_transaction_id"]
    status = event_data["posting_instruction_batch"]["status"]
    update_timestamp = event_data["posting_instruction_batch"]["insertion_timestamp"]
    # Remove extra microseconds
    original_date_time_without_microseconds = update_timestamp[:23] + update_timestamp[-1]
    migration_timestamp = datetime.strptime(original_date_time_without_microseconds, "%Y-%m-%dT%H:%M:%S.%fZ")
    posting_instruction_batch_id = event_data["posting_instruction_batch"]["id"]
    client_id=event_data["posting_instruction_batch"]["client_id"]
    client_batch_id=event_data["posting_instruction_batch"]["client_batch_id"]
    instruction_details=str(event_data["posting_instruction_batch"]["posting_instructions"][0]["instruction_details"])
    # #TODO Remove when external_transaction_id is correckty extracted from batch_details. So far feeding Athena batch_details field is not possible
    # # Convert batch_details to a JSON string
    batch_details_str = str(event_data["posting_instruction_batch"]["batch_details"])
    batch_details_str = batch_details_str.replace("'", '"')
    # # Check if batch_details_str is empty
    # if batch_details_str.strip() == '':
    #     batch_details = {}
    # else:
    #     batch_details = json.loads(batch_details_str)   
    # # Assign a default value if external_transaction_id is not present
    # external_transaction_id = batch_details.get('external_transaction_id', 'external_transaction_id_VALUE_NOT_PRESENT')    
    # global_reconciliator_id = batch_details.get('global_reconciliator_id', 'global_reconciliator_id_VALUE_NOT_PRESENT')    
    external_transaction_id = event_data.get("posting_instruction_batch", {}).get("batch_details", {}).get("external_transaction_id", "external_transaction_id_VALUE_NOT_PRESENT")     
    global_reconciliator_id = event_data.get("posting_instruction_batch", {}).get("batch_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT")  
    value_timestamp=event_data["posting_instruction_batch"]["value_timestamp"]
    booking_timestamp=event_data["posting_instruction_batch"]["booking_timestamp"]
    source_insert_timestamp=event_data["posting_instruction_batch"]["source_insertion_timestamp"]     
    phase=event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["phase"]
    asset=event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["asset"] 
    amount=event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["amount"] 
    denomination=event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["denomination"] 
    account_address=event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["account_address"] 
    account_sequence_number=event_data.get('account_sequence_number')
    # if("inbound_hard_settlement" in event_data["posting_instruction_batch"]["posting_instructions"][0]):
    #     # advice=str(event_data["posting_instruction_batch"]["posting_instructions"][0]["inbound_hard_settlement"]["advice"])
    #     credit="False"
    #     target_account_id = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["account_id"]
    #     credit_account_address = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["account_address"]
    #     internal_account_id= event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][1]["account_id"]
    #     debit_account_address = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][1]["account_address"]   
    # elif("custom_instruction" in event_data["posting_instruction_batch"]["posting_instructions"][0]):
    #     # advice=str(event_data["posting_instruction_batch"]["posting_instructions"][0]["inbound_hard_settlement"]["advice"])
    #     target_account_id = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["account_id"]
    #     credit_account_address = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["account_address"]
    #     internal_account_id= event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][1]["account_id"]
    #     debit_account_address = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][1]["account_address"]
    # elif("outbound_hard_settlement" in event_data["posting_instruction_batch"]["posting_instructions"][0]):
    #     # advice=str(event_data["posting_instruction_batch"]["posting_instructions"][0]["outbound_hard_settlement"]["advice"])
    #     credit="True"
    #     target_account_id = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][1]["account_id"]
    #     credit_account_address = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][1]["account_address"]
    #     internal_account_id= event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["account_id"]
    #     debit_account_address = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["account_address"]    

    creditor_account_id = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["account_id"]
    credit_account_address = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][0]["account_address"]
    debitor_account_id= event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][1]["account_id"]
    debit_account_address = event_data["posting_instruction_batch"]["posting_instructions"][0]["committed_postings"][1]["account_address"]   
    target_account_id = event_data.get('target_account_id')
    
    if("inbound_hard_settlement" in event_data["posting_instruction_batch"]["posting_instructions"][0]):
        credit="False"
    elif("outbound_hard_settlement" in event_data["posting_instruction_batch"]["posting_instructions"][0]):
        credit="True"

    try:
        posting_reconciliator_data['id']+=[client_transaction_id]
        posting_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
        posting_reconciliator_data['client_batch_id']+=[client_batch_id]
        posting_reconciliator_data['migration_status']+=[status]
        posting_reconciliator_data['migration_timestamp']+=[migration_timestamp]
        posting_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]
        # print(f"reconciliator_data: {posting_reconciliator_data}")
        
        posting_master_data['client_id']+=[client_id]
        posting_master_data['client_batch_id']+=[client_batch_id]
        posting_master_data['client_transaction_id']+=[client_transaction_id]
        posting_master_data['amount']+=[amount]
        posting_master_data['denomination']+=[denomination]
        # posting_master_data['target_account_id']+=[target_account_id]
        posting_master_data['creditor_account_id']+=[creditor_account_id]
        posting_master_data['credit_account_address']+=[credit_account_address]
        posting_master_data['debit_account_address']+=[debit_account_address]
        posting_master_data['advice']+=[advice]
        # posting_master_data['internal_account_id']+=[internal_account_id]
        posting_master_data['debitor_account_id']+=[debitor_account_id]
        posting_master_data['instruction_details']+=[instruction_details]
        posting_master_data['batch_details']+=[batch_details_str]
        posting_master_data['credit']+=[credit]
        posting_master_data['account_address']+=[account_address]
        posting_master_data['asset']+=[asset]
        posting_master_data['phase']+=[phase]
        posting_master_data['value_timestamp']+=[value_timestamp]
        posting_master_data['booking_timestamp']+=[booking_timestamp]
        posting_master_data['source_insert_timestamp']+=[source_insert_timestamp]
        posting_master_data['external_transaction_id']+=[external_transaction_id]
        posting_master_data['account_sequence_number']+=[str(account_sequence_number)]
        posting_master_data['global_reconciliator_id']+=[global_reconciliator_id]
        posting_master_data['posting_instruction_batch_id']+=[posting_instruction_batch_id]
        posting_master_data['target_account_id']+=[target_account_id]
    except Exception as e:
        print(f"Error during update or copy: {e}")
        
def handle_errored_postings(event_data,posting_reconciliator_data):
    update_status = event_data["posting_instruction_batch"]["error"]["type"]
    status_message= event_data["posting_instruction_batch"]["error"]["message"]
    posting_violations=event_data.get("posting_instruction_batch", {}).get("posting_instructions", [{}])[0].get("posting_violations", [])
    status=f"{update_status}; {status_message}; {posting_violations}"
    client_batch_id=event_data["posting_instruction_batch"]["client_batch_id"]
    client_transaction_id=event_data["posting_instruction_batch"]["posting_instructions"][0]["client_transaction_id"]
    global_reconciliator_id = event_data.get("posting_instruction_batch", {}).get("batch_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT")  
    try:
        posting_reconciliator_data['id']+=[client_transaction_id]
        posting_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
        posting_reconciliator_data['client_batch_id']+=[client_batch_id]
        posting_reconciliator_data['migration_status']+=[status]
        posting_reconciliator_data['migration_timestamp']+=[datetime.now()]
        posting_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]
        # print(f"reconciliator_data: {posting_reconciliator_data}")
    except Exception as e:
        print(f"Error during update or copy: {e}")
    
def handle_dlq_postings(event_data,posting_reconciliator_data):
    logging.info("dict insert")
    status = "DLQ: wrong request format or invalid enum values"
    client_batch_id=event_data["posting_instruction_batch"]["client_batch_id"]
    client_transaction_id=event_data["posting_instruction_batch"]["posting_instructions"][0]["client_transaction_id"]
    global_reconciliator_id = event_data.get("posting_instruction_batch", {}).get("batch_details", {}).get("global_reconciliator_id", "global_reconciliator_id_VALUE_NOT_PRESENT") 
    try:
        posting_reconciliator_data['id']+=[client_transaction_id]
        posting_reconciliator_data['global_reconciliator_id']+=[global_reconciliator_id]
        posting_reconciliator_data['client_batch_id']+=[client_batch_id]
        posting_reconciliator_data['migration_status']+=[status]
        posting_reconciliator_data['migration_timestamp']+=[datetime.now()]
        posting_reconciliator_data['reconciliation_timestamp']+=[datetime.now()]
        # print(f"reconciliator_data: {posting_reconciliator_data}")
    except Exception as e:
        print(f"Error during update or copy: {e}")
    logging.info("dict insert completed")

    
def contains_substring(string, substring):
    return substring in string


def insert_retry_policy_data(entity,sesion):
    entity_dict={
        "entity":[entity],
        "execution_timestamp":[datetime.now()]
    }
    insert_data_dict(sesion,entity_dict,'retry_policy_temp','retry_policy')  
    
    
def handle_account_balance(event_data,account_balance_master_data):
    event_id = event_data["event_id"]
    timestamp = event_data["timestamp"]
    related_resource_type = event_data['related_resource'].get('type')
    related_resource_id = event_data['related_resource'].get('id')
    sequence_number = event_data['related_resource'].get('sequence_number')
    migrated = event_data["migrated"]
    try:
        for balances in event_data["balances"]:
            if balances.get("posting_instruction_batch_id"):
                # If posting_instruction_batch_id field is not empty it contains account balance information
                id = balances.get('id')
                account_id = balances.get('account_id')
                account_address = balances.get('account_address')
                phase = balances.get('phase')
                asset = balances.get('asset')
                denomination = balances.get('denomination')
                posting_instruction_batch_id = balances.get('posting_instruction_batch_id')
                value_time = balances.get('value_time')
                amount = balances.get('amount')
                total_debit = balances.get('total_debit')
                total_credit = balances.get('total_credit')

                account_balance_master_data['event_id']+=[event_id]
                account_balance_master_data['id']+=[id]
                account_balance_master_data['account_id']+=[account_id]
                account_balance_master_data['account_address']+=[account_address]
                account_balance_master_data['phase']+=[phase]
                account_balance_master_data['asset']+=[asset]
                account_balance_master_data['denomination']+=[denomination]
                account_balance_master_data['posting_instruction_batch_id']+=[posting_instruction_batch_id]
                account_balance_master_data['value_time']+=[value_time]
                account_balance_master_data['amount']+=[amount]
                account_balance_master_data['total_debit']+=[total_debit]
                account_balance_master_data['total_credit']+=[total_credit]
                account_balance_master_data['timestamp']+=[timestamp]
                account_balance_master_data['related_resource_type']+=[related_resource_type]
                account_balance_master_data['related_resource_id']+=[related_resource_id]                
                account_balance_master_data['sequence_number']+=[sequence_number]
                account_balance_master_data['migrated']+=[str(migrated)]
        
            # print(account_balance_master_data)
    except Exception as e:
        print(f"Error during update or copy: {e}")
       
               
                                        
   
        

       
               
                                        
   
        

