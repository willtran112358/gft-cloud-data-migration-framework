module "sns_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sns_role_role-policy"
  policy             = data.aws_iam_policy_document.glue_policy.json
  name               = "${var.prefix}-AWSGlueServiceRole"
  assume_role_policy = data.aws_iam_policy_document.glue_assume_policy.json

}

module "lambdas_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-lambdas-role-policy"
  policy             = data.aws_iam_policy_document.lambdas_role_policy.json
  name               = "${var.prefix}-lambdas-role"
  assume_role_policy = data.aws_iam_policy_document.lambdas_assume_policy.json

}
################Step Functions Roles################
module "sf_invoke_crawler_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_invoke_crawler-role-policy"
  policy             = data.aws_iam_policy_document.sf-invoke-crawler_policy.json
  name               = "${var.prefix}-sf-invoke-crawler-role"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_customer_raw_migration_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_customer_raw_migration-policy"
  policy             = data.aws_iam_policy_document.sf_raw_staging_policy.json
  name               = "${var.prefix}-sf-customer-raw-migration"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_account_raw_migration_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_account_raw_migration-policy"
  policy             = data.aws_iam_policy_document.sf_raw_staging_policy.json
  name               = "${var.prefix}-sf-account-raw-migration"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_posting_raw_migration_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_posting_raw_migration-policy"
  policy             = data.aws_iam_policy_document.sf_raw_staging_policy.json
  name               = "${var.prefix}-sf-posting-raw-migration"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_deposit_raw_migration_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_deposit_raw_migration-policy"
  policy             = data.aws_iam_policy_document.sf_raw_staging_policy.json
  name               = "${var.prefix}-sf-deposit-raw-migration"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_loan_raw_migration_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_loan_raw_migration-policy"
  policy             = data.aws_iam_policy_document.sf_raw_staging_policy.json
  name               = "${var.prefix}-sf-loan-raw-migration"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_deploy_job_producer_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_deploy_job_producer-policy"
  policy             = data.aws_iam_policy_document.sf_deploy_job_producer_policy.json
  name               = "${var.prefix}-sf-deploy_job_producer"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_all_entities_dq_only_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_all_entities_dq_only-policy"
  policy             = data.aws_iam_policy_document.sf_raw_staging_policy.json
  name               = "${var.prefix}-sf-all-entities-dq-only"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_retry_listener_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_retry_listener-policy"
  policy             = data.aws_iam_policy_document.sf_raw_staging_policy.json
  name               = "${var.prefix}-sf-retry-listener"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_global_migration_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_global_migration_role-policy"
  policy             = data.aws_iam_policy_document.sf_raw_staging_policy.json
  name               = "${var.prefix}-sf_global_migration_role"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}

module "sf_od_postgres_to_s3_role" {
  source             = "../modules/L1/iam-role"
  iam_policy_name    = "${var.prefix}-sf_od_postgres_to_s3_role-policy"
  policy             = data.aws_iam_policy_document.sf_raw_staging_policy.json
  name               = "${var.prefix}-od_postgres_to_s3_role"
  assume_role_policy = data.aws_iam_policy_document.sf-assume-role.json

}
