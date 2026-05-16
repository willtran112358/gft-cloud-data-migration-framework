# ...

resource "aws_sfn_state_machine" "sf_invoke_crawler" {
  depends_on = [module.sf_invoke_crawler_role]
  definition = templatefile("stepfunctions/sf_invoke_crawler.asl.json",
    {
      sf_invoke_global_reconciliation = aws_sfn_state_machine.sf_global_reconciliation.arn
    }
  )
  name     = "${var.prefix}-sf-invoke-crawler"
  role_arn = module.sf_invoke_crawler_role.iam_role_arn
  tags = {
    "stateMachine:createdBy" = "SAM"
  }
  tags_all = {
    "stateMachine:createdBy" = "SAM"
  }
  type = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-invoke-crawler-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}

# ...
resource "aws_sfn_state_machine" "sf_invoke_all_crawler" {
  depends_on = [module.sf_invoke_crawler_role]
  definition = templatefile("stepfunctions/sf_invoke_all_crawler.asl.json",
    {
      sf_invoke_all_crawler = aws_sfn_state_machine.sf_invoke_crawler.arn
    }
  )
  name     = "${var.prefix}-sf-invoke-all-crawler"
  role_arn = module.sf_invoke_crawler_role.iam_role_arn
  tags = {
    "stateMachine:createdBy" = "SAM"
  }
  tags_all = {
    "stateMachine:createdBy" = "SAM"
  }
  type = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-invoke-all-crawler-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}

resource "aws_sfn_state_machine" "sf_customer_raw_to_migration" {
  definition = templatefile("stepfunctions/sf_customer_raw_to_migration.asl.json",
    {
      lambda-customer-reconciliation-files-raw         = aws_lambda_function.lambda-customer-reconciliation-files-raw.function_name,
      glue-job-raw-to-staging                          = aws_glue_job.raw_to_staging.name,
      lambda-customer-reconciliation-raw-staging       = aws_lambda_function.lambda-customer-reconciliation-raw-staging.function_name,
      customer-staging-migrationdb                     = aws_glue_job.customer_staging_migrationdb.name,
      lambda-customer-reconciliation-staging-migration = aws_lambda_function.lambda-customer-reconciliation-staging-migration.function_name,
      sql_query1                                       = "DELETE from ${aws_glue_catalog_database.tm_migration_database-staging.name}.customer",
      sql_query2                                       = "DELETE from ${aws_glue_catalog_database.tm_migration_database-migration.name}.customer"
    }
  )
  name     = "${var.prefix}_sf_customer_raw_to_migration"
  role_arn = module.sf_customer_raw_migration_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-customer-raw-migration-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = false
  }
}

resource "aws_sfn_state_machine" "sf_customer_staging_to_migration" {
  definition = templatefile("stepfunctions/sf_customer_staging_to_migration.asl.json",
    {
      customer-staging-migrationdb                     = aws_glue_job.customer_staging_migrationdb.name,
      lambda-customer-reconciliation-staging-migration = aws_lambda_function.lambda-customer-reconciliation-staging-migration.function_name,
      sql_query2                                       = "DELETE from ${aws_glue_catalog_database.tm_migration_database-migration.name}.customer"
    }
  )

  name     = "${var.prefix}_sf_customer_staging_to_migration"
  role_arn = module.sf_customer_raw_migration_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-customer-raw-migration-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = false
  }
}


resource "aws_sfn_state_machine" "sf_account_raw_to_migration" {
  definition = templatefile("stepfunctions/sf_account_raw_to_migration.asl.json",
    {
      lambda-account-reconciliation-files-raw         = aws_lambda_function.lambda-account-reconciliation-files-raw.function_name,
      account-raw-to-staging                          = "account-raw-to-staging",
      lambda-account-reconciliation-raw-staging       = aws_lambda_function.lambda-account-reconciliation-raw-staging.function_name,
      account-staging-migrationdb                     = aws_glue_job.account_staging_migrationdb.name,
      lambda-account-reconciliation-staging-migration = aws_lambda_function.lambda-account-reconciliation-staging-migration.function_name,
      sql_query1                                      = "DELETE from ${aws_glue_catalog_database.tm_migration_database-staging.name}.account",
      sql_query2                                      = "DELETE from ${aws_glue_catalog_database.tm_migration_database-migration.name}.aux_account WHERE id IN (SELECT id from ${aws_glue_catalog_database.tm_migration_database-staging.name}.account)"

    }
  )
  name     = "${var.prefix}_sf_account_raw_to_migration"
  role_arn = module.sf_account_raw_migration_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-account-raw-migration-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = false
  }
}

resource "aws_sfn_state_machine" "sf_posting_raw_to_migration" {
  definition = templatefile("stepfunctions/sf_posting_raw_to_migration.asl.json",
    {
      lambda-posting-reconciliation-files-raw         = aws_lambda_function.lambda-posting-reconciliation-files-raw.function_name,
      posting-raw-to-staging                          = "posting-raw-to-staging",
      lambda-posting-reconciliation-raw-staging       = aws_lambda_function.lambda-posting-reconciliation-raw-staging.function_name,
      posting-staging-migrationdb                     = aws_glue_job.posting_staging_migrationdb.name,
      lambda-posting-reconciliation-staging-migration = aws_lambda_function.lambda-posting-reconciliation-staging-migration.function_name,
      sql_query1                                      = "DELETE from ${aws_glue_catalog_database.tm_migration_database-staging.name}.posting",
      sql_query2                                      = "DELETE from ${aws_glue_catalog_database.tm_migration_database-migration.name}.aux_posting_instruction_batch"

    }
  )
  name     = "${var.prefix}_sf_posting_raw_to_migration"
  role_arn = module.sf_posting_raw_migration_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-posting-raw-migration-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = false
  }
}

resource "aws_sfn_state_machine" "sf_deposit_raw_to_migration" {
  definition = templatefile("stepfunctions/sf_deposit_raw_to_migration.asl.json",
    {
      lambda-deposit-reconciliation-files-raw         = aws_lambda_function.lambda-deposit-reconciliation-files-raw.function_name,
      deposit-raw-to-staging                          = "deposit-raw-to-staging",
      lambda-deposit-reconciliation-raw-staging       = aws_lambda_function.lambda-deposit-reconciliation-raw-staging.function_name,
      deposit-staging-migrationdb                     = aws_glue_job.deposit_staging_migrationdb.name,
      lambda-deposit-reconciliation-staging-migration = aws_lambda_function.lambda-deposit-reconciliation-staging-migration.function_name,
      sql_query1                                      = "DELETE from ${aws_glue_catalog_database.tm_migration_database-staging.name}.deposit",
      sql_query2                                      = "select * from  ${aws_glue_catalog_database.tm_migration_database-staging.name}.deposit" # Dummy query to mantain the same structure in all step functions

    }
  )
  name     = "${var.prefix}_sf_deposit_raw_to_migration"
  role_arn = module.sf_deposit_raw_migration_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-deposit-raw-migration-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = false
  }
}

resource "aws_sfn_state_machine" "sf_loan_raw_to_migration" {
  definition = templatefile("stepfunctions/sf_loan_raw_to_migration.asl.json",
    {
      lambda-loan-reconciliation-files-raw         = aws_lambda_function.lambda-loan-reconciliation-files-raw.function_name,
      loan-raw-to-staging                          = "loan-raw-to-staging",
      lambda-loan-reconciliation-raw-staging       = aws_lambda_function.lambda-loan-reconciliation-raw-staging.function_name,
      loan-staging-migrationdb                     = aws_glue_job.loan_staging_migrationdb.name,
      lambda-loan-reconciliation-staging-migration = aws_lambda_function.lambda-loan-reconciliation-staging-migration.function_name,
      sql_query1                                   = "DELETE from ${aws_glue_catalog_database.tm_migration_database-staging.name}.loan",
      sql_query2                                   = "select * from  ${aws_glue_catalog_database.tm_migration_database-staging.name}.loan" # Dummy query to mantain the same structure in all step functions

    }
  )
  name     = "${var.prefix}_sf_loan_raw_to_migration"
  role_arn = module.sf_loan_raw_migration_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-loan-raw-migration-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = false
  }
}

### Step Function for execute job producer customer ###
resource "aws_sfn_state_machine" "sf_deploy_job_producer_customer" {
  depends_on = [module.sf-deploy-job-customer-producer-log-group]
  definition = templatefile("stepfunctions/sf_deploy_job_producer_customer.asl.json",
    {
      eks_endpoint                          = var.eks_endpoint,
      sf_deploy_job_producer_customer_image = var.sf_deploy_job_producer_customer_image
    }
  )
  name     = "${var.prefix}_sf_deploying_job_producer_customer"
  role_arn = module.sf_deploy_job_producer_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-deploy-job-customer-producer-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}

### Step Function for execute job producer account ###
resource "aws_sfn_state_machine" "sf_deploy_job_producer_account" {
  depends_on = [module.sf-deploy-job-account-producer-log-group]
  definition = templatefile("stepfunctions/sf_deploy_job_producer_account.asl.json",
    {
      eks_endpoint                         = var.eks_endpoint,
      sf_deploy_job_producer_account_image = var.sf_deploy_job_producer_account_image
    }
  )
  name     = "${var.prefix}_sf_deploying_job_producer_account"
  role_arn = module.sf_deploy_job_producer_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-deploy-job-account-producer-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}

### Step Function for execute job producer posting ###
resource "aws_sfn_state_machine" "sf_deploy_job_producer_posting" {
  depends_on = [module.sf-deploy-job-posting-producer-log-group]
  definition = templatefile("stepfunctions/sf_deploy_job_producer_posting.asl.json",
    {
      eks_endpoint                         = var.eks_endpoint,
      sf_deploy_job_producer_posting_image = var.sf_deploy_job_producer_posting_image
    }
  )
  name     = "${var.prefix}_sf_deploying_job_producer_posting"
  role_arn = module.sf_deploy_job_producer_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-deploy-job-posting-producer-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}

### Step Function for DQ Only Jobs ###
resource "aws_sfn_state_machine" "sf_all_entities_dq_only" {
  definition = templatefile("stepfunctions/sf_all_entities_dq_only.asl.json",
    {
      name_job_customer     = aws_glue_job.customer_dq_only.name,
      name_job_account      = aws_glue_job.account_dq_only.name,
      name_job_posting      = aws_glue_job.posting_dq_only.name,
      name_job_deposit      = aws_glue_job.deposit_dq_only.name,
      name_job_loan         = aws_glue_job.loan_dq_only.name,
      sf_invoke_all_crawler = aws_sfn_state_machine.sf_invoke_all_crawler.arn

    }
  )
  name     = "${var.prefix}_sf_all_entities_dq_only"
  role_arn = module.sf_all_entities_dq_only_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-all-entities-dq-only.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}

### Step Function for execute Global Reconciliation Process ###
resource "aws_sfn_state_machine" "sf_global_reconciliation" {
  definition = templatefile("stepfunctions/sf_global_reconciliation.asl.json",
    {
      eks_endpoint                = var.eks_endpoint,
      global_reconciliation_image = var.global_reconciliation_image
    }
  )

  name     = "${var.prefix}_sf_global_reconciliation"
  role_arn = module.sf_deploy_job_producer_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf_global_reconciliation.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}

### Step Function for Retry process ###
resource "aws_sfn_state_machine" "sf_retry_listener" {
  definition = templatefile("stepfunctions/sf_retry_listener.asl.json",
    {
      lambda_retry = aws_lambda_function.lambda-retries.function_name,
    }
  )

  name     = "${var.prefix}_sf_retry_listener"
  role_arn = module.sf_retry_listener_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf_retry_listener.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}

### Step Function GLOBAL MIGRATION MAIN PROCESS ###
resource "aws_sfn_state_machine" "sf_global_migration" {
  definition = templatefile("stepfunctions/sf_global_migration.asl.json",
    {
      lambda_retry                        = aws_lambda_function.lambda-retries.function_name,
      lambda-start-stop-dates             = aws_lambda_function.lambda-start-stop-dates.function_name,
      sf_invoke_all_crawler               = aws_sfn_state_machine.sf_invoke_all_crawler.arn,
      sf_customer_raw_to_migration        = aws_sfn_state_machine.sf_customer_raw_to_migration.arn,
      sf_account_raw_to_migration         = aws_sfn_state_machine.sf_account_raw_to_migration.arn,
      sf_deposit_raw_to_migration         = aws_sfn_state_machine.sf_deposit_raw_to_migration.arn,
      sf_loan_raw_to_migration            = aws_sfn_state_machine.sf_loan_raw_to_migration.arn,
      sf_posting_raw_to_migration         = aws_sfn_state_machine.sf_posting_raw_to_migration.arn,
      lambda-history                      = aws_lambda_function.lambda-history.function_name,
      job-account-tm-id-matcher           = aws_glue_job.account_tm_id_matcher.name,
      job-posting-tm-id-matcher           = aws_glue_job.posting_tm_id_matcher.name,
      sf_deploy_job_producer_customer     = aws_sfn_state_machine.sf_deploy_job_producer_customer.arn,
      sf_invoke_retry_listener            = aws_sfn_state_machine.sf_retry_listener.arn,
      sf_deploy_job_producer_account      = aws_sfn_state_machine.sf_deploy_job_producer_account.arn,
      sf_deploy_job_producer_posting      = aws_sfn_state_machine.sf_deploy_job_producer_posting.arn,
      lambda-count-unreconcilied-entities = aws_lambda_function.lambda-count-unreconcilied-entities.function_name,
      sf_invoke_global_reconciliation     = aws_sfn_state_machine.sf_global_reconciliation.arn


    }
  )

  name     = "${var.prefix}_sf_global_migration"
  role_arn = module.sf_global_migration_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf_global_migration.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}


### Step Function GLOBAL MIGRATION MAIN PROCESS (CUSTOMER) ###
resource "aws_sfn_state_machine" "sf_global_migration_customer_demo" {
  definition = templatefile("stepfunctions/sf_global_migration_customer_demo.asl.json",
    {
      lambda_retry                        = aws_lambda_function.lambda-retries.function_name,
      lambda-start-stop-dates             = aws_lambda_function.lambda-start-stop-dates.function_name,
      sf_invoke_all_crawler               = aws_sfn_state_machine.sf_invoke_all_crawler.arn,
      sf_customer_raw_to_migration        = aws_sfn_state_machine.sf_customer_raw_to_migration.arn,
      lambda-history                      = aws_lambda_function.lambda-history.function_name,
      sf_deploy_job_producer_customer     = aws_sfn_state_machine.sf_deploy_job_producer_customer.arn,
      sf_invoke_retry_listener            = aws_sfn_state_machine.sf_retry_listener.arn,
      lambda-count-unreconcilied-entities = aws_lambda_function.lambda-count-unreconcilied-entities.function_name,
      sf_invoke_global_reconciliation     = aws_sfn_state_machine.sf_global_reconciliation.arn


    }
  )

  name     = "${var.prefix}_sf_global_migration_customer_demo"
  role_arn = module.sf_global_migration_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf_global_migration.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}


### Step Function GLOBAL MIGRATION MAIN PROCESS (CUSTOMER) ###
resource "aws_sfn_state_machine" "sf_global_migration_customer_demo_postgres" {
  definition = templatefile("stepfunctions/sf_global_migration_customer_demo_postgres.asl.json",
    {
      lambda_retry                        = aws_lambda_function.lambda-retries.function_name,
      lambda-start-stop-dates             = aws_lambda_function.lambda-start-stop-dates.function_name,
      sf_invoke_all_crawler               = aws_sfn_state_machine.sf_invoke_all_crawler.arn,
      sf_customer_staging_to_migration    = aws_sfn_state_machine.sf_customer_staging_to_migration.arn,
      lambda-history                      = aws_lambda_function.lambda-history.function_name,
      sf_deploy_job_producer_customer     = aws_sfn_state_machine.sf_deploy_job_producer_customer.arn,
      sf_invoke_retry_listener            = aws_sfn_state_machine.sf_retry_listener.arn,
      lambda-count-unreconcilied-entities = aws_lambda_function.lambda-count-unreconcilied-entities.function_name,
      sf_invoke_global_reconciliation     = aws_sfn_state_machine.sf_global_reconciliation.arn,
      glue-job-postgres-to-s3             = aws_glue_job.postgres_to_s3.name

    }
  )

  name     = "${var.prefix}_sf_global_migration_customer_demo_postgres"
  role_arn = module.sf_global_migration_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf_global_migration.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = true
  }
}
resource "aws_sfn_state_machine" "sf_od_data_postgres_to_s3" {
  definition = templatefile("stepfunctions/sf_od_data_postgres_to_s3.asl.json",
    {
      pg_host               = var.input_database_host,
      pg_port                          = var.input_database_port,
      pg_user               = var.input_database_user,
      pg_secret_name                     = var.input_database_secret_name,
      pg_database = var.input_database_db_name,
      pg_schema                                       = var.input_database_schema_name,
      output_s3                                       = var.postgres_to_s3_output_bucket
      postgres-to-s3-generic = aws_glue_job.generic_postgres_to_s3.name
    }
  )
  name     = "${var.prefix}_sf_od_data_postgres_to_s3"
  role_arn = module.sf_od_postgres_to_s3_role.iam_role_arn
  tags     = {}
  tags_all = {}
  type     = "STANDARD"

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${module.sf-od-postgres-to-s3-log-group.log_group_arn}:*"
  }

  tracing_configuration {
    enabled = false
  }
}