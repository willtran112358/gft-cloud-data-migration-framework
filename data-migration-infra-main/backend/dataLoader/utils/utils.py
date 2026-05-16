import sys
import os
current_dir = os.path.dirname(__file__)
library_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(library_dir)

def get_event_status(event_type,msg):
    if (event_type=="ACCOUNT_UPDATED_EVENT"):
        if('account_created' in msg):
            return msg['account_created']['account']['status']
        else:
            return msg['account_updated']['account']['status']
    elif (event_type=="RESOURCE_MIGRATED"):
        return msg['resource_migrated']['vault_resource_loaded']['resource_status']
    elif (event_type=="RESOURCE_BATCH_RESPONSE"):
        return msg["status"]
    elif (event_type=="POSTING_RESPONSE"):
        return msg["posting_instruction_batch"]["status"]
    elif (event_type=="DLQ" or event_type=="DLQ_POSTINGS"):
        return "NOT_STATUS"
    elif (event_type=="ACCOUNT_BALANCE_EVENT"):
        return "DEFAULT"
    else:
        return "not send"
    
def get_resource_type(event_type,msg):
    if (event_type=="ACCOUNT_UPDATED_EVENT"):
        return "ACCOUNT_RESOURCE"
    elif (event_type=="RESOURCE_MIGRATED"):
        if ('account_resource' in msg['resource_migrated']['resource']):
            return "ACCOUNT_RESOURCE"
        else:
            return "CUSTOMER_RESOURCE"
    elif (event_type=="RESOURCE_BATCH_RESPONSE"):
        if ('account_resource' in msg['resources'][0]):
            return "ACCOUNT_RESOURCE"
        else:
            return "CUSTOMER_RESOURCE"
    elif (event_type=="DLQ"):
        if ('account_resource' in msg['resource_batch']['resources'][0]):
            return "ACCOUNT_RESOURCE"
        else:
            return "CUSTOMER_RESOURCE"
    elif (event_type=="DLQ_POSTINGS" or event_type=="POSTING_RESPONSE"):
        return "POSTING_RESOURCE"
    elif (event_type=="ACCOUNT_BALANCE_EVENT"):
        return "ACCOUNT_BALANCE_RESOURCE"
        
def valid_status(status,event_type, resource_type):
    if status=="ACCOUNT_STATUS_OPENING":
        return False
    elif status=="RESOURCE_STATUS_PENDING":
        return False
    elif status=="RESOURCE_BATCH_STATUS_PENDING":
        return False
    elif status=="RESOURCE_STATUS_LOADED" and event_type=="RESOURCE_MIGRATED" and resource_type=="ACCOUNT_RESOURCE": 
        return False
    else:
        return True
    
def migration_event_filter(event_data,event_type,resource_type):
    if event_type == "DLQ":
        # Check if "global_reconciliator_id" exists in additional_details.
        # Only events from migration contain such key, otherwise transaction doesn't belong to migration and it is skipped.
        # Finding it in the first record of the batch is enough
        # if resource_type in ( "ACCOUNT_RESOURCE", "CUSTOMER_RESOURCE"):
        print("DLQ ACCOUNT_RESOURCE DLQ")
        first_resource = event_data.get("resource_batch", {}).get("resources", [{}])[0]
        if resource_type =="CUSTOMER_RESOURCE":
            if first_resource.get(resource_type.lower()).get("additional_details", {}).get("global_reconciliator_id"):
                # print("Process event due belongs to a migration")
                return True  
        elif resource_type =="ACCOUNT_RESOURCE":
            print("resource_type ACCOUNT_RESOURCE DLQ")
            if first_resource.get(resource_type.lower()).get("account", {}).get("details", {}).get("global_reconciliator_id"):
                # print("Process event due belongs to a migration")
                return True                          
    elif event_type =="DLQ_POSTINGS":
        if event_data.get("posting_instruction_batch", {}).get("batch_details", {}).get("global_reconciliator_id"):
            # print("Process event due belongs to a migration")
            return True    
    elif event_type=="ACCOUNT_BALANCE_EVENT":
        if event_data.get("migrated") is True:
            # print("Process event due belongs to a migration")
            return True
    if event_type =="POSTING_RESPONSE":
        if event_data.get("posting_instruction_batch", {}).get("batch_details", {}).get("global_reconciliator_id"): 
            # print("Process event due belongs to a migration")
            return True       
    elif event_type =="RESOURCE_BATCH_RESPONSE":
        # Check if "global_reconciliator_id" exists in additional_details.
        # Only events from migration contain such key, otherwise transaction doesn't belong to migration and it is skipped.
        # Finding it in the first record of the batch is enough
        first_resource = event_data.get("resources", [{}])[0]
        if resource_type =="CUSTOMER_RESOURCE":
            if first_resource.get(resource_type.lower(), {}).get("additional_details", {}).get("global_reconciliator_id"):
                # print("Process event due belongs to a migration")
                return True        
        elif resource_type =="ACCOUNT_RESOURCE":
            if first_resource.get(resource_type.lower(), {}).get("account", {}).get("details", {}).get("global_reconciliator_id"):
                # print("Process event due belongs to a migration")
                return True             
    elif event_type =="ACCOUNT_UPDATED_EVENT":
        if event_data.get("account_updated", {}).get("account", {}).get("details", {}).get("global_reconciliator_id"): 
            # print("Process event due belongs to a migration")
            return True       
    elif event_type == "RESOURCE_MIGRATED":
        if resource_type =="CUSTOMER_RESOURCE":        
            if event_data.get("resource_migrated", {}).get("resource", {}).get(resource_type.lower(), {}).get("additional_details", {}).get("global_reconciliator_id") :
                # print("Process event due belongs to a migration")
                return True    
        elif resource_type =="ACCOUNT_RESOURCE":
            if event_data.get("resource_migrated", {}).get("resource", {}).get(resource_type.lower(), {}).get("account", {}).get("details", {}).get("global_reconciliator_id"):
                # print("Process event due belongs to a migration")
                return True   