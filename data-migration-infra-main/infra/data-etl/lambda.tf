################Lambda reconciliation files against raw table################
### Customer ###
data "archive_file" "lambda-reconciliation-files-raw" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-files-raw.py"
  output_path = "${path.module}/python/lambda-reconciliation-files-raw.zip"
}

resource "aws_lambda_function" "lambda-customer-reconciliation-files-raw" {

  filename      = "${path.module}/python/lambda-reconciliation-files-raw.zip"
  function_name = lower("${var.prefix}-lambda-customer-reconciliation-files-raw")
  description   = "Lambda function to count the records in source files (customers) and compare them with his correspondant table"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-files-raw.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME   = var.region
      BUCKET_NAME   = module.s3_source_files.bucket_id
      ATHENA_BUCKET = "s3://${module.s3_athena_queries.bucket_id}/"
      ID            = "id"
      TABLE_NAME    = "customer"
      DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-raw.name
      FOLDER_PATH   = "customer/"
      LOG_DB        = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE     = "logs_table"
      STAGE         = "RAW"
      ENTITY        = "customer"
      FAILURE_RATE  = var.reconciliator_failure_rate
    }
  }
}

################Lambda reconciliation files against raw table################
### Account ###
data "archive_file" "lambda-accounts-reconciliation-files-raw" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-files-raw.py"
  output_path = "${path.module}/python/lambda-reconciliation-files-raw.zip"
}

resource "aws_lambda_function" "lambda-account-reconciliation-files-raw" {

  filename      = "${path.module}/python/lambda-reconciliation-files-raw.zip"
  function_name = lower("${var.prefix}-lambda-accounts-reconciliation-files-raw")
  description   = "Lambda function to count the records in source files (account) and compare them with his correspondant table"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-files-raw.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME   = var.region
      BUCKET_NAME   = module.s3_source_files.bucket_id
      ATHENA_BUCKET = "s3://${module.s3_athena_queries.bucket_id}/"
      ID            = "id"
      TABLE_NAME    = "account"
      DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-raw.name
      FOLDER_PATH   = "account/"
      LOG_DB        = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE     = "logs_table"
      STAGE         = "RAW"
      ENTITY        = "account"
      FAILURE_RATE  = var.reconciliator_failure_rate
    }
  }
}

################Lambda reconciliation files against raw table################
### Posting ###
data "archive_file" "lambda-posting-reconciliation-files-raw" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-files-raw.py"
  output_path = "${path.module}/python/lambda-reconciliation-files-raw.zip"
}

resource "aws_lambda_function" "lambda-posting-reconciliation-files-raw" {

  filename      = "${path.module}/python/lambda-reconciliation-files-raw.zip"
  function_name = lower("${var.prefix}-lambda-posting-reconciliation-files-raw")
  description   = "Lambda function to count the records in source files (posting) and compare them with his correspondant table"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-files-raw.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME   = var.region
      BUCKET_NAME   = module.s3_source_files.bucket_id
      ATHENA_BUCKET = "s3://${module.s3_athena_queries.bucket_id}/"
      ID            = "target_account_id"
      TABLE_NAME    = "posting"
      DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-raw.name
      FOLDER_PATH   = "posting_instruction_batch/"
      LOG_DB        = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE     = "logs_table"
      STAGE         = "RAW"
      ENTITY        = "posting"
      FAILURE_RATE  = var.reconciliator_failure_rate
    }
  }
}

################Lambda reconciliation files against raw table################
### deposit ###
data "archive_file" "lambda-deposit-reconciliation-files-raw" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-files-raw.py"
  output_path = "${path.module}/python/lambda-reconciliation-files-raw.zip"
}

resource "aws_lambda_function" "lambda-deposit-reconciliation-files-raw" {

  filename      = "${path.module}/python/lambda-reconciliation-files-raw.zip"
  function_name = lower("${var.prefix}-lambda-deposit-reconciliation-files-raw")
  description   = "Lambda function to count the records in source files (posting) and compare them with his correspondant table"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-files-raw.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME   = var.region
      BUCKET_NAME   = module.s3_source_files.bucket_id
      ATHENA_BUCKET = "s3://${module.s3_athena_queries.bucket_id}/"
      ID            = "id"
      TABLE_NAME    = "deposit"
      DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-raw.name
      FOLDER_PATH   = "deposit/"
      LOG_DB        = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE     = "logs_table"
      STAGE         = "RAW"
      ENTITY        = "deposit"
      FAILURE_RATE  = var.reconciliator_failure_rate
    }
  }
}

################Lambda reconciliation files against raw table################
### loan ###
data "archive_file" "lambda-loan-reconciliation-files-raw" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-files-raw.py"
  output_path = "${path.module}/python/lambda-reconciliation-files-raw.zip"
}

resource "aws_lambda_function" "lambda-loan-reconciliation-files-raw" {

  filename      = "${path.module}/python/lambda-reconciliation-files-raw.zip"
  function_name = lower("${var.prefix}-lambda-loan-reconciliation-files-raw")
  description   = "Lambda function to count the records in source files (posting) and compare them with his correspondant table"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-files-raw.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME   = var.region
      BUCKET_NAME   = module.s3_source_files.bucket_id
      ATHENA_BUCKET = "s3://${module.s3_athena_queries.bucket_id}/"
      ID            = "codcontrat"
      TABLE_NAME    = "loan"
      DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-raw.name
      FOLDER_PATH   = "loan/"
      LOG_DB        = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE     = "logs_table"
      STAGE         = "RAW"
      ENTITY        = "loan"
      FAILURE_RATE  = var.reconciliator_failure_rate
    }
  }
}


#Lambda reconciliation Raw against Staging table
#customer
data "archive_file" "lambda-reconciliation-raw-staging" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-raw-staging.py"
  output_path = "${path.module}/python/lambda-reconciliation-raw-staging.zip"
}

resource "aws_lambda_function" "lambda-customer-reconciliation-raw-staging" {

  filename      = "${path.module}/python/lambda-reconciliation-raw-staging.zip"
  function_name = lower("${var.prefix}-lambda-customer-reconciliation-raw-staging")
  description   = "Lambda function to count the unique records by id in raw table and compare them with his correspondant table in staging"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-raw-staging.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME           = var.region
      BUCKET_NAME           = module.s3_source_files.bucket_id
      ATHENA_BUCKET         = "s3://${module.s3_athena_queries.bucket_id}/"
      ID                    = "id"
      TABLE_NAME            = "customer"
      RAW_DATABASE_NAME     = aws_glue_catalog_database.tm_migration_database-raw.name
      STAGING_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-staging.name
      FOLDER_PATH           = "customer/"
      LOG_DB                = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE             = "logs_table"
      STAGE                 = "STAGING"
      ENTITY                = "customer"
      FAILURE_RATE          = var.reconciliator_failure_rate
    }
  }
}

#account
resource "aws_lambda_function" "lambda-account-reconciliation-raw-staging" {

  filename      = "${path.module}/python/lambda-reconciliation-raw-staging.zip"
  function_name = lower("${var.prefix}-lambda-account-reconciliation-raw-staging")
  description   = "Lambda function to count the unique records by id in raw table and compare them with his correspondant table in staging"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-raw-staging.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME           = var.region
      BUCKET_NAME           = module.s3_source_files.bucket_id
      ATHENA_BUCKET         = "s3://${module.s3_athena_queries.bucket_id}/"
      ID                    = "id"
      TABLE_NAME            = "account"
      RAW_DATABASE_NAME     = aws_glue_catalog_database.tm_migration_database-raw.name
      STAGING_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-staging.name
      FOLDER_PATH           = "account/"
      LOG_DB                = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE             = "logs_table"
      STAGE                 = "STAGING"
      ENTITY                = "account"
      FAILURE_RATE          = var.reconciliator_failure_rate
    }
  }
}

#posting
resource "aws_lambda_function" "lambda-posting-reconciliation-raw-staging" {

  filename      = "${path.module}/python/lambda-reconciliation-raw-staging.zip"
  function_name = lower("${var.prefix}-lambda-posting-reconciliation-raw-staging")
  description   = "Lambda function to count the unique records by id in raw table and compare them with his correspondant table in staging"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-raw-staging.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME           = var.region
      BUCKET_NAME           = module.s3_source_files.bucket_id
      ATHENA_BUCKET         = "s3://${module.s3_athena_queries.bucket_id}/"
      ID                    = "target_account_id"
      TABLE_NAME            = "posting"
      RAW_DATABASE_NAME     = aws_glue_catalog_database.tm_migration_database-raw.name
      STAGING_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-staging.name
      FOLDER_PATH           = "posting_instruction_batch/"
      LOG_DB                = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE             = "logs_table"
      STAGE                 = "STAGING"
      ENTITY                = "posting"
      FAILURE_RATE          = var.reconciliator_failure_rate
    }
  }
}


#deposit
resource "aws_lambda_function" "lambda-deposit-reconciliation-raw-staging" {

  filename      = "${path.module}/python/lambda-reconciliation-raw-staging.zip"
  function_name = lower("${var.prefix}-lambda-deposit-reconciliation-raw-staging")
  description   = "Lambda function to count the unique records by id in raw table and compare them with his correspondant table in staging"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-raw-staging.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME           = var.region
      BUCKET_NAME           = module.s3_source_files.bucket_id
      ATHENA_BUCKET         = "s3://${module.s3_athena_queries.bucket_id}/"
      ID                    = "id"
      TABLE_NAME            = "deposit"
      RAW_DATABASE_NAME     = aws_glue_catalog_database.tm_migration_database-raw.name
      STAGING_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-staging.name
      FOLDER_PATH           = "deposit/"
      LOG_DB                = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE             = "logs_table"
      STAGE                 = "STAGING"
      ENTITY                = "deposit"
      FAILURE_RATE          = var.reconciliator_failure_rate
    }
  }
}

#loan
data "archive_file" "lambda-loan-reconciliation-raw-staging" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-loan-raw-staging.py"
  output_path = "${path.module}/python/lambda-reconciliation-loan-raw-staging.zip"
}

resource "aws_lambda_function" "lambda-loan-reconciliation-raw-staging" {

  filename      = "${path.module}/python/lambda-reconciliation-loan-raw-staging.zip"
  function_name = lower("${var.prefix}-lambda-loan-reconciliation-raw-staging")
  description   = "Lambda function to count the unique records by id in raw table and compare them with his correspondant table in staging"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-loan-raw-staging.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME           = var.region
      BUCKET_NAME           = module.s3_source_files.bucket_id
      ATHENA_BUCKET         = "s3://${module.s3_athena_queries.bucket_id}/"
      ID_RAW                = "codcontrat"
      ID_STAGING            = "account_id"
      TABLE_NAME_RAW        = "loan"
      TABLE_NAME_STAGING    = "loan"
      STAGING_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-staging.name
      RAW_DATABASE_NAME     = aws_glue_catalog_database.tm_migration_database-raw.name
      FOLDER_PATH           = "loan/"
      LOG_DB                = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE             = "logs_table"
      STAGE                 = "STAGING"
      ENTITY                = "loan"
      FAILURE_RATE          = var.reconciliator_failure_rate
    }
  }
}

#Lambda reconciliation Staging against Magration table
#customer
data "archive_file" "lambda-reconciliation-staging-migration" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-staging-migration.py"
  output_path = "${path.module}/python/lambda-reconciliation-staging-migration.zip"
}

data "archive_file" "lambda-reconciliation-posting-staging-migration" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-posting-staging-migration.py"
  output_path = "${path.module}/python/lambda-reconciliation-posting-staging-migration.zip"
}

data "archive_file" "lambda-reconciliation-deposit-staging-migration" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-deposit-staging-migration.py"
  output_path = "${path.module}/python/lambda-reconciliation-deposit-staging-migration.zip"
}

data "archive_file" "lambda-reconciliation-loan-staging-migration" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-reconciliation-loan-staging-migration.py"
  output_path = "${path.module}/python/lambda-reconciliation-loan-staging-migration.zip"
}

resource "aws_lambda_function" "lambda-customer-reconciliation-staging-migration" {

  filename      = "${path.module}/python/lambda-reconciliation-staging-migration.zip"
  function_name = lower("${var.prefix}-lambda-customer-reconciliation-staging-migration")
  description   = "Lambda function to count the unique records by id in staging customer table and compare them with his correspondant table in migration"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-staging-migration.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME             = var.region
      BUCKET_NAME             = module.s3_source_files.bucket_id
      ATHENA_BUCKET           = "s3://${module.s3_athena_queries.bucket_id}/"
      ID_STAGING              = "id"
      ID_MIGRATION            = "id"
      TABLE_NAME_STAGING      = "customer"
      TABLE_NAME_MIGRATION    = "customer"
      MIGRATION_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-migration.name
      STAGING_DATABASE_NAME   = aws_glue_catalog_database.tm_migration_database-staging.name
      FOLDER_PATH             = "customer/"
      LOG_DB                  = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE               = "logs_table"
      STAGE                   = "MIGRATION"
      ENTITY                  = "customer"
      FAILURE_RATE            = var.reconciliator_failure_rate
    }
  }
}

#account
resource "aws_lambda_function" "lambda-account-reconciliation-staging-migration" {

  filename      = "${path.module}/python/lambda-reconciliation-staging-migration.zip"
  function_name = lower("${var.prefix}-lambda-account-reconciliation-staging-migration")
  description   = "Lambda function to count the unique records by id in staging customer table and compare them with his correspondant table in migration"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-staging-migration.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME             = var.region
      BUCKET_NAME             = module.s3_source_files.bucket_id
      ATHENA_BUCKET           = "s3://${module.s3_athena_queries.bucket_id}/"
      ID_STAGING              = "id"
      ID_MIGRATION            = "id"
      TABLE_NAME_STAGING      = "account"
      TABLE_NAME_MIGRATION    = "aux_account"
      MIGRATION_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-migration.name
      STAGING_DATABASE_NAME   = aws_glue_catalog_database.tm_migration_database-staging.name
      FOLDER_PATH             = "account/"
      LOG_DB                  = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE               = "logs_table"
      STAGE                   = "MIGRATION"
      ENTITY                  = "account"
      FAILURE_RATE            = var.reconciliator_failure_rate
    }
  }
}

#posting

resource "aws_lambda_function" "lambda-posting-reconciliation-staging-migration" {

  filename      = "${path.module}/python/lambda-reconciliation-posting-staging-migration.zip"
  function_name = lower("${var.prefix}-lambda-posting-reconciliation-staging-migration")
  description   = "Lambda function to count the unique records by id in staging customer table and compare them with his correspondant table in migration"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-posting-staging-migration.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME             = var.region
      BUCKET_NAME             = module.s3_source_files.bucket_id
      ATHENA_BUCKET           = "s3://${module.s3_athena_queries.bucket_id}/"
      ID_STAGING              = "target_account_id"
      ID_MIGRATION            = "target_account_id"
      TABLE_NAME_STAGING      = "posting"
      TABLE_NAME_MIGRATION    = "aux_posting_instruction_batch"
      MIGRATION_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-migration.name
      STAGING_DATABASE_NAME   = aws_glue_catalog_database.tm_migration_database-staging.name
      FOLDER_PATH             = "posting_instruction_batch/"
      LOG_DB                  = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE               = "logs_table"
      STAGE                   = "MIGRATION"
      ENTITY                  = "posting"
      FAILURE_RATE            = var.reconciliator_failure_rate
    }
  }
}


#deposit
resource "aws_lambda_function" "lambda-deposit-reconciliation-staging-migration" {

  filename      = "${path.module}/python/lambda-reconciliation-deposit-staging-migration.zip"
  function_name = lower("${var.prefix}-lambda-deposit-reconciliation-staging-migration")
  description   = "Lambda function to count the unique records by id in staging customer table and compare them with his correspondant table in migration"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-deposit-staging-migration.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME             = var.region
      BUCKET_NAME             = module.s3_source_files.bucket_id
      ATHENA_BUCKET           = "s3://${module.s3_athena_queries.bucket_id}/"
      ID_STAGING              = "id"
      ID_MIGRATION            = "id"
      TABLE_NAME_STAGING      = "deposit"
      TABLE_NAME_MIGRATION    = "aux_account"
      MIGRATION_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-migration.name
      STAGING_DATABASE_NAME   = aws_glue_catalog_database.tm_migration_database-staging.name
      FOLDER_PATH             = "deposit/"
      LOG_DB                  = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE               = "logs_table"
      STAGE                   = "MIGRATION"
      ENTITY                  = "deposit"
      FAILURE_RATE            = var.reconciliator_failure_rate
    }
  }
}

#loan
resource "aws_lambda_function" "lambda-loan-reconciliation-staging-migration" {

  filename      = "${path.module}/python/lambda-reconciliation-loan-staging-migration.zip"
  function_name = lower("${var.prefix}-lambda-loan-reconciliation-staging-migration")
  description   = "Lambda function to count the unique records by id in staging customer table and compare them with his correspondant table in migration"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-reconciliation-loan-staging-migration.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME             = var.region
      BUCKET_NAME             = module.s3_source_files.bucket_id
      ATHENA_BUCKET           = "s3://${module.s3_athena_queries.bucket_id}/"
      ID_STAGING              = "account_id"
      ID_MIGRATION            = "id"
      TABLE_NAME_STAGING      = "loan"
      TABLE_NAME_MIGRATION    = "aux_account"
      MIGRATION_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-migration.name
      STAGING_DATABASE_NAME   = aws_glue_catalog_database.tm_migration_database-staging.name
      FOLDER_PATH             = "loan/"
      LOG_DB                  = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE               = "logs_table"
      STAGE                   = "MIGRATION"
      ENTITY                  = "loan"
      FAILURE_RATE            = var.reconciliator_failure_rate
    }
  }
}

################ Lambda to create and store records in history tables ################
data "archive_file" "lambda-history" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-history.py"
  output_path = "${path.module}/python/lambda-history.zip"
}

resource "aws_lambda_function" "lambda-history" {

  filename      = "${path.module}/python/lambda-history.zip"
  function_name = lower("${var.prefix}-lambda-history")
  description   = "Lambda to create and store records in history tables"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-history.lambda_handler"
  runtime       = "python3.9"
  timeout       = 900
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME       = var.region
      ATHENA_BUCKET     = "s3://${module.s3_athena_queries.bucket_id}/"
      S3_BUCKET_RAW     = "s3://${module.s3_raw.bucket_id}/"
      S3_BUCKET_STAGING = "s3://${module.s3_staging.bucket_id}/"
    }
  }
}

################ Lambda to continuosly when reconciliator API finish to process an entitie ################
data "archive_file" "lambda-retries" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-retries.py"
  output_path = "${path.module}/python/lambda-retries.zip"
}

resource "aws_lambda_function" "lambda-retries" {

  filename      = "${path.module}/python/lambda-retries.zip"
  function_name = lower("${var.prefix}-lambda-retries")
  description   = "Lambda to create and store records in history tables"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-retries.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME   = var.region
      ATHENA_BUCKET = "s3://${module.s3_athena_queries.bucket_id}/"
      DB            = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE     = "logs_table"
      TABLE_POLICY  = "retry_policy"
    }
  }
}

################ Lambda to store start and stop dates in log table for each execution of the global sf ################
data "archive_file" "lambda-start-stop-dates" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-start-stop-dates.py"
  output_path = "${path.module}/python/lambda-start-stop-dates.zip"
}

resource "aws_lambda_function" "lambda-start-stop-dates" {

  filename      = "${path.module}/python/lambda-start-stop-dates.zip"
  function_name = lower("${var.prefix}-lambda-start-stop-dates")
  description   = "Lambda to store start and stop dates in log table for each execution of the global sf"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-start-stop-dates.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME   = var.region
      ATHENA_BUCKET = "s3://${module.s3_athena_queries.bucket_id}/"
      DB            = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE     = "logs_table"
    }
  }
}

################ Lambda to check if master tables are empties or not ################
data "archive_file" "lambda-count-unreconcilied-entities" {
  type        = "zip"
  source_file = "${path.module}/python/lambda-count-unreconcilied-entities.py"
  output_path = "${path.module}/python/lambda-count-unreconcilied-entities.zip"
}

resource "aws_lambda_function" "lambda-count-unreconcilied-entities" {

  filename      = "${path.module}/python/lambda-count-unreconcilied-entities.zip"
  function_name = lower("${var.prefix}-lambda-count-unreconcilied-entities")
  description   = "Lambda to check if master tables are empties or not"
  role          = module.lambdas_role.iam_role_arn
  handler       = "lambda-count-unreconcilied-entities.lambda_handler"
  runtime       = "python3.9"
  timeout       = 180
  layers        = [var.aws_lambda_pandas_layer]

  kms_key_arn = local.kms_lambda_arn
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      REGION_NAME             = var.region
      ATHENA_BUCKET           = "s3://${module.s3_athena_queries.bucket_id}/"
      MIGRATION_DATABASE_NAME = aws_glue_catalog_database.tm_migration_database-migration.name
      LOG_TABLE               = "logs_table"
    }
  }
}