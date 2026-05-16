<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.5 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 4.67 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | 2.4.2 |
| <a name="provider_aws"></a> [aws](#provider\_aws) | 4.67.0 |
| <a name="provider_terraform"></a> [terraform](#provider\_terraform) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_lambda-account-reconciliation-files-raw-log-group"></a> [lambda-account-reconciliation-files-raw-log-group](#module\_lambda-account-reconciliation-files-raw-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_lambda-count-unreconcilied-entities-log-group"></a> [lambda-count-unreconcilied-entities-log-group](#module\_lambda-count-unreconcilied-entities-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_lambda-customer-reconciliation-files-raw-log-group"></a> [lambda-customer-reconciliation-files-raw-log-group](#module\_lambda-customer-reconciliation-files-raw-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_lambda-deposit-reconciliation-files-raw-log-group"></a> [lambda-deposit-reconciliation-files-raw-log-group](#module\_lambda-deposit-reconciliation-files-raw-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_lambda-history-log-group"></a> [lambda-history-log-group](#module\_lambda-history-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_lambda-loan-reconciliation-files-raw-log-group"></a> [lambda-loan-reconciliation-files-raw-log-group](#module\_lambda-loan-reconciliation-files-raw-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_lambda-posting-reconciliation-files-raw-log-group"></a> [lambda-posting-reconciliation-files-raw-log-group](#module\_lambda-posting-reconciliation-files-raw-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_lambda-retries-log-group"></a> [lambda-retries-log-group](#module\_lambda-retries-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_lambda-start-stop-dates-log-group"></a> [lambda-start-stop-dates-log-group](#module\_lambda-start-stop-dates-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_lambdas_role"></a> [lambdas\_role](#module\_lambdas\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_lambdas_security_group"></a> [lambdas\_security\_group](#module\_lambdas\_security\_group) | ../modules/L2/security-group | n/a |
| <a name="module_s3_athena_queries"></a> [s3\_athena\_queries](#module\_s3\_athena\_queries) | ../modules/L1/s3-private | n/a |
| <a name="module_s3_migration"></a> [s3\_migration](#module\_s3\_migration) | ../modules/L1/s3-private | n/a |
| <a name="module_s3_raw"></a> [s3\_raw](#module\_s3\_raw) | ../modules/L1/s3-private | n/a |
| <a name="module_s3_source_files"></a> [s3\_source\_files](#module\_s3\_source\_files) | ../modules/L1/s3-private | n/a |
| <a name="module_s3_staging"></a> [s3\_staging](#module\_s3\_staging) | ../modules/L1/s3-private | n/a |
| <a name="module_sf-account-raw-migration-log-group"></a> [sf-account-raw-migration-log-group](#module\_sf-account-raw-migration-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-all-entities-dq-only"></a> [sf-all-entities-dq-only](#module\_sf-all-entities-dq-only) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-customer-raw-migration-log-group"></a> [sf-customer-raw-migration-log-group](#module\_sf-customer-raw-migration-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-deploy-job-account-producer-log-group"></a> [sf-deploy-job-account-producer-log-group](#module\_sf-deploy-job-account-producer-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-deploy-job-customer-producer-log-group"></a> [sf-deploy-job-customer-producer-log-group](#module\_sf-deploy-job-customer-producer-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-deploy-job-deposit-producer-log-group"></a> [sf-deploy-job-deposit-producer-log-group](#module\_sf-deploy-job-deposit-producer-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-deploy-job-loan-producer-log-group"></a> [sf-deploy-job-loan-producer-log-group](#module\_sf-deploy-job-loan-producer-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-deploy-job-posting-producer-log-group"></a> [sf-deploy-job-posting-producer-log-group](#module\_sf-deploy-job-posting-producer-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-deposit-raw-migration-log-group"></a> [sf-deposit-raw-migration-log-group](#module\_sf-deposit-raw-migration-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-invoke-all-crawler-log-group"></a> [sf-invoke-all-crawler-log-group](#module\_sf-invoke-all-crawler-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-invoke-crawler-log-group"></a> [sf-invoke-crawler-log-group](#module\_sf-invoke-crawler-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-loan-raw-migration-log-group"></a> [sf-loan-raw-migration-log-group](#module\_sf-loan-raw-migration-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf-posting-raw-migration-log-group"></a> [sf-posting-raw-migration-log-group](#module\_sf-posting-raw-migration-log-group) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf_account_raw_migration_role"></a> [sf\_account\_raw\_migration\_role](#module\_sf\_account\_raw\_migration\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sf_all_entities_dq_only_role"></a> [sf\_all\_entities\_dq\_only\_role](#module\_sf\_all\_entities\_dq\_only\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sf_customer_raw_migration_role"></a> [sf\_customer\_raw\_migration\_role](#module\_sf\_customer\_raw\_migration\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sf_deploy_job_producer_role"></a> [sf\_deploy\_job\_producer\_role](#module\_sf\_deploy\_job\_producer\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sf_deposit_raw_migration_role"></a> [sf\_deposit\_raw\_migration\_role](#module\_sf\_deposit\_raw\_migration\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sf_global_migration"></a> [sf\_global\_migration](#module\_sf\_global\_migration) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf_global_migration_role"></a> [sf\_global\_migration\_role](#module\_sf\_global\_migration\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sf_global_reconciliation"></a> [sf\_global\_reconciliation](#module\_sf\_global\_reconciliation) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf_invoke_crawler_role"></a> [sf\_invoke\_crawler\_role](#module\_sf\_invoke\_crawler\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sf_loan_raw_migration_role"></a> [sf\_loan\_raw\_migration\_role](#module\_sf\_loan\_raw\_migration\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sf_posting_raw_migration_role"></a> [sf\_posting\_raw\_migration\_role](#module\_sf\_posting\_raw\_migration\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sf_retry_listener"></a> [sf\_retry\_listener](#module\_sf\_retry\_listener) | ../modules/L1/cloudwatch-log-group | n/a |
| <a name="module_sf_retry_listener_role"></a> [sf\_retry\_listener\_role](#module\_sf\_retry\_listener\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_sns_role"></a> [sns\_role](#module\_sns\_role) | ../modules/L1/iam-role | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_glue_catalog_database.tm_migration_database-migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_catalog_database) | resource |
| [aws_glue_catalog_database.tm_migration_database-raw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_catalog_database) | resource |
| [aws_glue_catalog_database.tm_migration_database-staging](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_catalog_database) | resource |
| [aws_glue_crawler.glue_crawler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_crawler) | resource |
| [aws_glue_crawler.glue_crawler_global_reconciliation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_crawler) | resource |
| [aws_glue_job.account_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.account_staging_migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.account_tm_id_matcher](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.customer_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.customer_staging_migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.deposit_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.deposit_staging_migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.loan_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.loan_staging_migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.posting_balance_calculator](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.posting_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.posting_staging_migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_glue_job.posting_tm_id_matcher](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) | resource |
| [aws_lambda_function.lambda-account-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-account-reconciliation-raw-staging](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-account-reconciliation-staging-migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-count-unreconcilied-entities](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-customer-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-customer-reconciliation-raw-staging](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-customer-reconciliation-staging-migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-deposit-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-deposit-reconciliation-raw-staging](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-deposit-reconciliation-staging-migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-history](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-loan-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-loan-reconciliation-raw-staging](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-loan-reconciliation-staging-migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-posting-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-posting-reconciliation-raw-staging](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-posting-reconciliation-staging-migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-retries](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.lambda-start-stop-dates](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_s3_object.account-job-staging-dq](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.account-job-staging-migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.account_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.account_tm_id_matcher](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.customer-job-staging-dq](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.customer-job-staging-migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.customer_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.deposit-job-staging-migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.deposit_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.loan-job-staging-migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.loan_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.posting-job-staging-dq](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.posting-job-staging-migrationdb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.posting_balance_calculator](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.posting_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.posting_tm_id_matcher](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_s3_object.s3_source_files_dirs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object) | resource |
| [aws_sfn_state_machine.sf_account_raw_to_migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_all_entities_dq_only](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_customer_raw_to_migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_deploy_job_producer_account](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_deploy_job_producer_customer](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_deploy_job_producer_posting](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_deposit_raw_to_migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_global_migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_global_reconciliation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_invoke_all_crawler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_invoke_crawler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_loan_raw_to_migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_posting_raw_to_migration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.sf_retry_listener](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sfn_state_machine) | resource |
| [archive_file.lambda-accounts-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-count-unreconcilied-entities](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-deposit-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-history](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-loan-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-loan-reconciliation-raw-staging](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-posting-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-reconciliation-deposit-staging-migration](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-reconciliation-files-raw](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-reconciliation-loan-staging-migration](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-reconciliation-posting-staging-migration](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-reconciliation-raw-staging](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-reconciliation-staging-migration](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-retries](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.lambda-start-stop-dates](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_eks_cluster.eks-cluster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/eks_cluster) | data source |
| [aws_iam_policy_document.glue_assume_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.glue_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.lambdas_assume_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.lambdas_role_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sf-assume-role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sf-invoke-crawler_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sf_deploy_job_producer_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sf_raw_staging_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_kms_alias.cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/kms_alias) | data source |
| [aws_vpc.networking_vpc](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/vpc) | data source |
| [terraform_remote_state.infra](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_lambda_pandas_layer"></a> [aws\_lambda\_pandas\_layer](#input\_aws\_lambda\_pandas\_layer) | aws lambda layer for pandas | `string` | n/a | yes |
| <a name="input_create_balance_calculator_job"></a> [create\_balance\_calculator\_job](#input\_create\_balance\_calculator\_job) | Flag to create the resource | `bool` | `false` | no |
| <a name="input_csv-raw-crawler-tags"></a> [csv-raw-crawler-tags](#input\_csv-raw-crawler-tags) | crawler tags group | `map(string)` | n/a | yes |
| <a name="input_data_migration_namespace"></a> [data\_migration\_namespace](#input\_data\_migration\_namespace) | data migration namespace | `string` | `"dataloader"` | no |
| <a name="input_eks_cluster_name"></a> [eks\_cluster\_name](#input\_eks\_cluster\_name) | eks cluster name | `string` | `"data-migration"` | no |
| <a name="input_eks_endpoint"></a> [eks\_endpoint](#input\_eks\_endpoint) | eks endpoint URL | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | proyect environment, user ct for control tower configurations | `string` | n/a | yes |
| <a name="input_global-reconciliation-crawler-tags"></a> [global-reconciliation-crawler-tags](#input\_global-reconciliation-crawler-tags) | tags group for global reconciliator crawlers | `map(string)` | n/a | yes |
| <a name="input_global_reconciliation_image"></a> [global\_reconciliation\_image](#input\_global\_reconciliation\_image) | ECR Image PATH form global reconciliator docker image | `string` | n/a | yes |
| <a name="input_iacgroup"></a> [iacgroup](#input\_iacgroup) | owner of the AWS resource | `string` | `"UnAssign"` | no |
| <a name="input_log_group_retention"></a> [log\_group\_retention](#input\_log\_group\_retention) | log group retention in days | `number` | `14` | no |
| <a name="input_number_of_workers"></a> [number\_of\_workers](#input\_number\_of\_workers) | number of workers, minimun is 2 | `number` | `2` | no |
| <a name="input_owner"></a> [owner](#input\_owner) | owner of the AWS resource | `string` | `"IT"` | no |
| <a name="input_prefix"></a> [prefix](#input\_prefix) | Prefix that is always at the beginning of the bucket name  and other components | `string` | `""` | no |
| <a name="input_private_subnets"></a> [private\_subnets](#input\_private\_subnets) | A list of private subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_public_subnets"></a> [public\_subnets](#input\_public\_subnets) | A list of public subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_reconciliator_failure_rate"></a> [reconciliator\_failure\_rate](#input\_reconciliator\_failure\_rate) | Failure acceptance percentage in reconciliations | `string` | `"0.5"` | no |
| <a name="input_region"></a> [region](#input\_region) | aws region | `string` | n/a | yes |
| <a name="input_s3_source_files_dirs"></a> [s3\_source\_files\_dirs](#input\_s3\_source\_files\_dirs) | list of names for s3 source files directories and crawler names | `set(string)` | <pre>[<br>  "customer",<br>  "account",<br>  "posting",<br>  "loan",<br>  "deposit"<br>]</pre> | no |
| <a name="input_sf_deploy_job_producer_account_image"></a> [sf\_deploy\_job\_producer\_account\_image](#input\_sf\_deploy\_job\_producer\_account\_image) | ECR Image PATH form sf deploy job producer account docker image | `string` | n/a | yes |
| <a name="input_sf_deploy_job_producer_customer_image"></a> [sf\_deploy\_job\_producer\_customer\_image](#input\_sf\_deploy\_job\_producer\_customer\_image) | ECR Image PATH form sf deploy job producer customer docker image | `string` | n/a | yes |
| <a name="input_sf_deploy_job_producer_posting_image"></a> [sf\_deploy\_job\_producer\_posting\_image](#input\_sf\_deploy\_job\_producer\_posting\_image) | ECR Image PATH form sf deploy job producer posting docker image | `string` | n/a | yes |
| <a name="input_sns_event_arn"></a> [sns\_event\_arn](#input\_sns\_event\_arn) | arn of sns event | `string` | n/a | yes |
| <a name="input_vpc_cidr"></a> [vpc\_cidr](#input\_vpc\_cidr) | vpc cidr | `string` | `""` | no |
| <a name="input_worker_type"></a> [worker\_type](#input\_worker\_type) | crawler tags group | `string` | `"G.1X"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_name"></a> [name](#output\_name) | n/a |
| <a name="output_sf-deploy-jobs-role-arn"></a> [sf-deploy-jobs-role-arn](#output\_sf-deploy-jobs-role-arn) | n/a |
<!-- END_TF_DOCS -->