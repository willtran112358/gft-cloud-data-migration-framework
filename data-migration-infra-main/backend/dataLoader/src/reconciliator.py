#lsof -i tcp:8000
#kill -9
#cd backend/dataLoader/src
#python3 -m uvicorn reconciliator:app --host 0.0.0.0 --port 8000 --reload
import sys
import os
import asyncio
current_dir = os.path.dirname(__file__)
library_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(library_dir)
from datetime import datetime
from utils.reconciliation_helper import compare_time,insert_data_dict,handle_account_updated,handle_customer_loaded,handle_dlq_resources,handle_resource_duplicated,handle_resource_failed,handle_migrated_postings,handle_errored_postings,handle_dlq_postings,handle_account_balance,insert_retry_policy_data
from fastapi import FastAPI, Request, Body, HTTPException, BackgroundTasks
from datetime import datetime, timedelta
from common.constants import (
  AWS_ACCESS_KEY_ID,
  AWS_SECRET_ACCESS_KEY,
  ASYNC_TIME,
  COMPARE_TIME
)
from  common.constants import REGION_NAME
import uvicorn
import logging
logging.basicConfig(level=logging.INFO)
import boto3
from utils.reconciliator_utils import generate_empty_master_account_dict,generate_empty_master_customer_dict,generate_empty_reconciliation_resource_dict, generate_empty_reconciliation_posting_dict, generate_empty_master_posting_dict,generate_empty_master_account_balance_dict
app = FastAPI()
sesion= boto3.Session(
        region_name=REGION_NAME
    )
customer_reconciliator_data = None
customer_master_data = None
account_master_data = None
account_reconciliator_data = None
posting_reconciliator_data = None
posting_master_data = None
sequence_time=datetime.now()
account_balance_master_data = None

async def background_task():
    global customer_reconciliator_data
    global account_reconciliator_data
    global customer_master_data
    global account_master_data
    global posting_reconciliator_data
    global posting_master_data
    global sequence_time
    global account_balance_master_data
    while True:
        await asyncio.sleep(ASYNC_TIME)
        logging.info("90 seconds waiting")
        if compare_time(ASYNC_TIME,sequence_time):
            logging.info("90 seconds check")
            if(customer_reconciliator_data!=None):
                if(len(customer_reconciliator_data['id'])>0):
                    insert_data_dict(sesion,customer_reconciliator_data,'customer_temp','reconciliation_customer')
                    customer_reconciliator_data = generate_empty_reconciliation_resource_dict()
                    sequence_time = datetime.now()
                    insert_retry_policy_data("customer",sesion)
            if(account_reconciliator_data!=None):
                if(len(account_reconciliator_data['id'])>0):
                    insert_data_dict(sesion,account_reconciliator_data,'account_temp','reconciliation_account')   
                    account_reconciliator_data = generate_empty_reconciliation_resource_dict()     
                    sequence_time = datetime.now()
                    insert_retry_policy_data("account",sesion) 
            if(customer_master_data!=None):
                if(len(customer_master_data['id'])>0):
                    insert_data_dict(sesion,customer_master_data,'customer_temp','master_customer')
                    customer_master_data = generate_empty_master_customer_dict()
                    sequence_time = datetime.now()
            if(account_master_data!=None):
                if(len(account_master_data['id'])>0):
                    insert_data_dict(sesion,account_master_data,'account_temp','master_account') 
                    account_master_data = generate_empty_master_account_dict()
                    sequence_time = datetime.now()
            if(posting_reconciliator_data!=None):
                if(len(posting_reconciliator_data['id'])>0):
                    insert_data_dict(sesion,posting_reconciliator_data,'posting_temp','reconciliation_posting_instruction_batch') 
                    posting_reconciliator_data = generate_empty_reconciliation_posting_dict()
                    sequence_time = datetime.now()  
                    insert_retry_policy_data("posting_instruction_batch",sesion) 
            if(posting_master_data!=None):
                if(len(posting_master_data['client_transaction_id'])>0):
                    insert_data_dict(sesion,posting_master_data,'posting_temp','master_posting_instruction_batch') 
                    posting_master_data = generate_empty_master_posting_dict()
                    sequence_time = datetime.now()    
            if(account_balance_master_data!=None):   
                if(len(account_balance_master_data['id'])>0):
                    insert_data_dict(sesion,account_balance_master_data,'account_balance_temp','master_account_balance') 
                    account_balance_master_data = generate_empty_master_account_balance_dict()
                    sequence_time = datetime.now()              
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_task())


@app.post("/validate_resource_batch/")
async def validate_resource_batch(event_type: str, resource_type:str, event_status: str, request: Request, data: dict = Body(...), ):
    logging.info(f"{event_type} - {resource_type} - {event_status} ")
    """
    This endpoint receives event data, validates it, and persists it to the
    appropriate destination table based on the provided resource_type parameter.
    """
    global customer_reconciliator_data
    global account_reconciliator_data
    global customer_master_data
    global account_master_data
    global posting_reconciliator_data
    global posting_master_data
    global sequence_time
    global account_balance_master_data
    if customer_reconciliator_data is None:
        customer_reconciliator_data=generate_empty_reconciliation_resource_dict()
        account_reconciliator_data=generate_empty_reconciliation_resource_dict()
        customer_master_data=generate_empty_master_customer_dict()
        account_master_data=generate_empty_master_account_dict()
        posting_reconciliator_data = generate_empty_reconciliation_posting_dict()
        posting_master_data = generate_empty_master_posting_dict()
        account_balance_master_data = generate_empty_master_account_balance_dict()

    """
    This endpoint receives event data and processes it based on the event type.
    """
    try:
        start= datetime.now()
        handle_event(data, event_type, resource_type, event_status)  # Assuming handle_event takes all four arguments
        end = datetime.now()
        logging.info(f"Start: {start}, After: {end}")
        return {"message": f"Successfully processed event of type: {resource_type}, {event_type}, {event_status}"}

    except (ValueError, Exception) as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def handle_event(event_data, event_type, resource_type, event_status) :
    global customer_reconciliator_data
    global account_reconciliator_data
    global customer_master_data
    global account_master_data
    global posting_reconciliator_data
    global posting_master_data
    global sequence_time
    global account_balance_master_data
    # event_type = identify_event(event_data)
    try:
        if event_type == "RESOURCE_MIGRATED" and resource_type == "CUSTOMER_RESOURCE" and event_status == "RESOURCE_STATUS_LOADED":
            #Success Customer Load into Vault 
            handle_customer_loaded(event_data,customer_reconciliator_data,customer_master_data)
            if compare_time(COMPARE_TIME,sequence_time):
                logging.info("inserting")
                insert_data_dict(sesion,customer_reconciliator_data,'customer_temp','reconciliation_customer')
                insert_data_dict(sesion,customer_master_data,'customer_temp','master_customer')
                customer_reconciliator_data = generate_empty_reconciliation_resource_dict()
                customer_master_data = generate_empty_master_customer_dict()
                sequence_time = datetime.now()
        elif event_type == "RESOURCE_MIGRATED" and event_status == "RESOURCE_STATUS_FAILED":
            #Failed Customer or Account Load into Vault 
            handle_resource_failed(event_data,resource_type,customer_reconciliator_data,account_reconciliator_data)
            if resource_type ==  "CUSTOMER_RESOURCE":        
                if compare_time(COMPARE_TIME,sequence_time):
                    logging.info("inserting")
                    insert_data_dict(sesion,customer_reconciliator_data,'customer_temp','reconciliation_customer')
                    customer_reconciliator_data = generate_empty_reconciliation_resource_dict()
                    sequence_time = datetime.now()
            
            elif resource_type ==  "ACCOUNT_RESOURCE":
                if compare_time(COMPARE_TIME,sequence_time):
                    logging.info("inserting")
                    insert_data_dict(sesion,account_reconciliator_data,'account_temp','reconciliation_account')
                    account_reconciliator_data = generate_empty_reconciliation_resource_dict()
                    sequence_time = datetime.now()
            
        elif event_type == "RESOURCE_BATCH_RESPONSE":
            #Customer and Account Resource batch response Rejected
            handle_resource_duplicated(event_data,resource_type,customer_reconciliator_data,account_reconciliator_data)
            if resource_type ==  "CUSTOMER_RESOURCE":
                if compare_time(COMPARE_TIME,sequence_time):
                    logging.info("inserting")
                    insert_data_dict(sesion,customer_reconciliator_data,'customer_temp','reconciliation_customer')
                    customer_reconciliator_data = generate_empty_reconciliation_resource_dict()   
                    sequence_time = datetime.now()
            elif resource_type ==  "ACCOUNT_RESOURCE":
                if compare_time(COMPARE_TIME,sequence_time):
                    logging.info("inserting")
                    insert_data_dict(sesion,account_reconciliator_data,'account_temp','reconciliation_account')
                    account_reconciliator_data = generate_empty_reconciliation_resource_dict()
                    sequence_time = datetime.now()
            
        elif event_type == "ACCOUNT_UPDATED_EVENT" and resource_type == "ACCOUNT_RESOURCE" and event_status == "ACCOUNT_STATUS_OPEN":
            #Success Account created Open into Vault
            handle_account_updated(event_data,account_reconciliator_data,account_master_data)
            if compare_time(COMPARE_TIME,sequence_time):
                insert_data_dict(sesion,account_reconciliator_data,'account_temp','reconciliation_account')
                insert_data_dict(sesion,account_master_data,'account_temp','master_account')
                account_reconciliator_data = generate_empty_reconciliation_resource_dict()  
                account_master_data = generate_empty_master_account_dict()
                sequence_time = datetime.now()
                        
        elif event_type == "DLQ":   
            
            handle_dlq_resources(event_data,customer_reconciliator_data,account_reconciliator_data,resource_type)
            if resource_type ==  "CUSTOMER_RESOURCE":
                if compare_time(COMPARE_TIME,sequence_time):
                    logging.info("inserting")
                    insert_data_dict(sesion,customer_reconciliator_data,'customer_temp','reconciliation_customer')
                    customer_reconciliator_data = generate_empty_reconciliation_resource_dict()   
                    sequence_time = datetime.now()
            elif resource_type ==  "ACCOUNT_RESOURCE":
                if compare_time(COMPARE_TIME,sequence_time):
                    logging.info("inserting")
                    insert_data_dict(sesion,account_reconciliator_data,'account_temp','reconciliation_account')
                    account_reconciliator_data = generate_empty_reconciliation_resource_dict() 
                    sequence_time = datetime.now()
        elif event_type == "POSTING_RESPONSE" and resource_type == "POSTING_RESOURCE":
            logging.info("posting detected")
            if event_status == "POSTING_INSTRUCTION_BATCH_STATUS_ACCEPTED":
                logging.info("posting acepted")        
                handle_migrated_postings(event_data,posting_reconciliator_data,posting_master_data)
                if compare_time(COMPARE_TIME,sequence_time):
                    insert_data_dict(sesion,posting_reconciliator_data,'posting_temp','reconciliation_posting_instruction_batch')
                    insert_data_dict(sesion,posting_master_data,'posting_temp','master_posting_instruction_batch')
                    posting_reconciliator_data = generate_empty_reconciliation_posting_dict()  
                    posting_master_data = generate_empty_master_posting_dict()
                    sequence_time = datetime.now()
            else:
                logging.info("errored posting detected")
                handle_errored_postings(event_data,posting_reconciliator_data)
                if compare_time(COMPARE_TIME,sequence_time):
                    insert_data_dict(sesion,posting_reconciliator_data,'posting_temp','reconciliation_posting_instruction_batch')
                    posting_reconciliator_data = generate_empty_reconciliation_posting_dict()  
                    sequence_time = datetime.now()
        elif event_type == "DLQ_POSTINGS" and resource_type == "POSTING_RESOURCE":
                logging.info("dlq posting detected")
                handle_dlq_postings(event_data,posting_reconciliator_data)
                if compare_time(COMPARE_TIME,sequence_time):
                    insert_data_dict(sesion,posting_reconciliator_data,'posting_temp','reconciliation_posting_instruction_batch')
                    posting_reconciliator_data = generate_empty_reconciliation_posting_dict()  
                    sequence_time = datetime.now()
        elif event_type == "ACCOUNT_BALANCE_EVENT" and resource_type == "ACCOUNT_BALANCE_RESOURCE" and event_status == "DEFAULT": 
                logging.info("handle account balance")
                handle_account_balance(event_data,account_balance_master_data)
                if compare_time(COMPARE_TIME,sequence_time):
                    insert_data_dict(sesion,account_balance_master_data,'account_balance_temp','master_account_balance')
                    account_balance_master_data = generate_empty_master_account_balance_dict()  
                    sequence_time = datetime.now()
        else:
            raise ValueError(f"Unsupported event type: {event_type}  resource type {resource_type} event status {event_status}")
    
    except Exception as e:
        # Log the error for debugging purposes
        logging.error(f"Error processing event: {str(e)}")
        # Raise the exception again to ensure the caller handles it
        raise e
        

if __name__ == "__main__":
    uvicorn.run("reconciliator:app", host="0.0.0.0", port=80, log_level="debug")