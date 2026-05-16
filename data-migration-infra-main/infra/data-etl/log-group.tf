### Step Function Log Groups ###

module "sf-invoke-crawler-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-invoke-crawler-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-invoke-all-crawler-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-invoke-all-crawler-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-customer-raw-migration-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-customer-raw-migration-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-account-raw-migration-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-account-raw-migration-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-posting-raw-migration-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-posting-raw-migration-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-deposit-raw-migration-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-deposit-raw-migration-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-loan-raw-migration-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-loan-raw-migration-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-deploy-job-customer-producer-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-deploy-job-customer-producer-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-deploy-job-account-producer-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-deploy-job-account-producer-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-deploy-job-posting-producer-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-deploy-job-posting-producer-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-deploy-job-deposit-producer-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-deploy-job-deposit-producer-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-deploy-job-loan-producer-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-deploy-job-loan-producer-log-group"
  retention_in_days      = var.log_group_retention
}

module "sf-all-entities-dq-only" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-all-entities-dq-only"
  retention_in_days      = var.log_group_retention
}

module "sf_global_reconciliation" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf_global_reconciliation"
  retention_in_days      = var.log_group_retention
}

module "sf_retry_listener" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf_retry_listener"
  retention_in_days      = var.log_group_retention
}

module "sf_global_migration" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf_global_migration"
  retention_in_days      = var.log_group_retention
}

### Lambda Log Groups ###

module "lambda-customer-reconciliation-files-raw-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/lambda/${var.prefix}-lambda-customer-reconciliation-files-raw"
  retention_in_days      = var.log_group_retention
}

module "lambda-account-reconciliation-files-raw-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/lambda/${var.prefix}-lambda-account-reconciliation-files-raw"
  retention_in_days      = var.log_group_retention
}

module "lambda-posting-reconciliation-files-raw-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/lambda/${var.prefix}-lambda-posting-reconciliation-files-raw"
  retention_in_days      = var.log_group_retention
}

module "lambda-deposit-reconciliation-files-raw-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/lambda/${var.prefix}-lambda-deposit-reconciliation-files-raw"
  retention_in_days      = var.log_group_retention
}

module "lambda-loan-reconciliation-files-raw-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/lambda/${var.prefix}-lambda-loan-reconciliation-files-raw"
  retention_in_days      = var.log_group_retention
}

module "lambda-history-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/lambda/${var.prefix}-lambda-history"
  retention_in_days      = var.log_group_retention
}

module "lambda-retries-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/lambda/${var.prefix}-lambda-retries"
  retention_in_days      = var.log_group_retention
}

module "lambda-start-stop-dates-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/lambda/${var.prefix}-lambda-start-stop-dates"
  retention_in_days      = var.log_group_retention
}

module "lambda-count-unreconcilied-entities-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/lambda/${var.prefix}-lambda-count-unreconcilied-entities"
  retention_in_days      = var.log_group_retention
}


module "sf-od-postgres-to-s3-log-group" {
  source = "../modules/L1/cloudwatch-log-group"

  cloudwatch_kms_key_arn = data.aws_kms_alias.cloudwatch.target_key_arn
  log_group_name         = "/aws/sf/sf-od-postgres-to-s3-log-group"
  retention_in_days      = var.log_group_retention
}