from datetime import datetime
import os

# Kafka config
BOOTSTRAP_SERVER = os.environ.get("BOOTSTRAP_SERVER", 'TBD,')
SECURITY_PROTOCOL = os.environ.get("SECURITY_PROTOCOL", "SASL_SSL")
SASL_MECHANISM = os.environ.get("SASL_MECHANISM", "SCRAM-SHA-512")
SASL_USERNAME = os.environ.get("SASL_USERNAME", "")
SASL_PASSWORD = os.environ.get("SASL_PASSWORD", "")

# Kafka topics
RESOURCE_BATCH_PRODUCER_TOPIC =  "vault.data_loader_api.v1.data_loader.resource_batch.create.requests"
PIB_PRODUCER_TOPIC="vault.migrations.postings.requests"
#Data Base

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "your_access_key_id")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "your_secret_access_key")
S3_BUCKET = os.environ.get("S3_BUCKET", 's3://<ACCOUNTID>-eu-central-1-gft-dm-development-athena-queries/queries-results/')
DATABASE_NAME = os.environ.get("DATABASE_NAME", 'development_migrationdb')
REGION_NAME = os.environ.get("REGION_NAME", 'eu-central-1')
WORKGROUP = os.environ.get("WORKGROUP", 'primary')

COMPARE_TIME=60
ASYNC_TIME=90

# RESOURCE_MIGRATED_MIGRATION_STATUSES = 'RESOURCE_STATUS_LOADED,RESOURCE_STATUS_FAILED'
# KO_RESOURCE_BATCH_MIGRATION_STATUSES = 'RESOURCE_BATCH_STATUS_REJECTED_RESOURCE_DUPLICATED,RESOURCE_BATCH_STATUS_REJECTED'

EVENT_TYPE={
    "vault.data_loader_api.v1.data_loader.resource_batch.create.requests.failures":"DLQ",
    "vault.data_loader_api.v1.data_loader.resource_batch.create.responses":"RESOURCE_BATCH_RESPONSE",
    "vault.data_loader_api.v1.data_loader.resource.migrated.events":"RESOURCE_MIGRATED",
    "vault.core_api.v2.accounts.account.events":"ACCOUNT_UPDATED_EVENT",
    "vault.migrations.postings.requests.dlq":"DLQ_POSTINGS",
    "vault.migrations.postings.responses":"POSTING_RESPONSE",
    "vault.core_api.v1.balances.account_balance.events":"ACCOUNT_BALANCE_EVENT"
    # "vault.api.v1.postings.posting_instruction_batch.created":"POSTING_MIGRATED"
}
RESOURCE_MAP={
    "CUSTOMER_RESOURCE": "customer",
    "ACCOUNT_RESOURCE": "account",
    "POSTING_RESOURCE": "posting"
}

VALID_EVENT_TYPES = ["RESOURCE_BATCH_RESPONSE", "RESOURCE_MIGRATED", "ACCOUNT_UPDATED_EVENT", "DLQ"]
VALID_RESOURCE_TYPES= ["CUSTOMER_RESOURCE", "ACCOUNT_RESOURCE"]
VALID_EVENT_STATUS= ["RESOURCE_BATCH_STATUS_REJECTED_RESOURCE_DUPLICATED",
                       "RESOURCE_BATCH_STATUS_REJECTED",
                       "RESOURCE_STATUS_LOADED",
                       "RESOURCE_STATUS_FAILED",
                       "ACCOUNT_STATUS_OPEN"] 
RESOURCE_BATCH_STATUSES_REJECTED = ["RESOURCE_BATCH_STATUS_REJECTED_RESOURCE_DUPLICATED", "RESOURCE_BATCH_STATUS_REJECTED"]



DEFAULT_CURR_ACC_PARAMETER_VALUES = {
    "account_holders_types": {
        "enumeration_value": "99"
    },
    "daily_withdrawal_limit_by_transaction_type": {
        "string_value": "{'ATM': '1000'}"
    },
    "inactivity_fee_application_day": {
        "decimal_value": "1"
    },
    "interest_application_day": {
        "decimal_value": "1"
    },
    "maintenance_fee_application_day": {
        "decimal_value": "1"
    },
    "minimum_balance_fee_application_day": {
        "decimal_value": "1"
    },
    "roundup_autosave_active": {
        "enumeration_value": "True"
    },
    "unarranged_overdraft_fee_application_day": {
        "decimal_value": "1"
    }
}

DEFAULT_CURR_TIMEDEPOSIT_PARAMETER_VALUES = {
    "fee_free_withdrawal_percentage_limit": {
		"decimal_value": "0"
    },
    "fixed_interest_rate": {
        "decimal_value":"2.5"
    },
    "interest_application_day": {
        "decimal_value": "18"
    },
    "term": {
        "decimal_value": "24"
    }
}

DEFAULT_CURR_LOAN_PARAMETER_VALUES = {
    "deposit_account": {
        "account_id_value": "1c11f6e8-3300-4c25-8c8b-d4dc4c9ff215"
    },
    "amortise_upfront_fee": {
        "enumeration_value":"True"
    },
    "fixed_interest_loan": {
        "enumeration_value":"True"
    },
    "fixed_interest_rate": {
        "decimal_value":"1.25"
    },
    "interest_accrual_rest_type": {
        "enumeration_value":"monthly"
    },
    "repayment_holiday_impact_preference": {
        "enumeration_value":"increase_emi"
    },
    "total_repayment_count": {
        "decimal_value":"25"
    },
    "principal": {
        "decimal_value":"10000"
    },
    "upfront_fee": {
        "decimal_value":"0"
    },
    "capitalise_late_repayment_fee": {
        "enumeration_value":"False"
    },
    "due_amount_calculation_day": {
        "decimal_value":"5"
    },
    "variable_rate_adjustment": {
        "decimal_value":"0"
    }
}
