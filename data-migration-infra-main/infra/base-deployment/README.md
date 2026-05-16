## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.5 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 4.67 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | ~> 4.67 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_base-deployments"></a> [base-deployments](#module\_base-deployments) | ../modules/L3/base-deployments | n/a |
| <a name="module_internal_list_fronent_ecr"></a> [internal\_list\_fronent\_ecr](#module\_internal\_list\_fronent\_ecr) | ../modules/L1/ecr | n/a |
| <a name="module_internal_list_server_ecr"></a> [internal\_list\_server\_ecr](#module\_internal\_list\_server\_ecr) | ../modules/L1/ecr | n/a |
| <a name="module_printsouts_ecr"></a> [printsouts\_ecr](#module\_printsouts\_ecr) | ../modules/L1/ecr | n/a |
| <a name="module_s3_access_logs"></a> [s3\_access\_logs](#module\_s3\_access\_logs) | ../modules/L1/s3-private | n/a |
| <a name="module_score_ecr"></a> [score\_ecr](#module\_score\_ecr) | ../modules/L1/ecr | n/a |
| <a name="module_sns_cis"></a> [sns\_cis](#module\_sns\_cis) | ../modules/L1/sns | n/a |
| <a name="module_sns_event_buckets"></a> [sns\_event\_buckets](#module\_sns\_event\_buckets) | ../modules/L1/sns | n/a |
| <a name="module_sns_role"></a> [sns\_role](#module\_sns\_role) | ../modules/L1/iam-role | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.s3-access-logs-policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sns_assume_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sns_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.topic](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_account_name"></a> [account\_name](#input\_account\_name) | aws account name | `string` | n/a | yes |
| <a name="input_accounts_read_ecr"></a> [accounts\_read\_ecr](#input\_accounts\_read\_ecr) | list of account that can read from shared services ECR | `list(string)` | n/a | yes |
| <a name="input_additional_contacts"></a> [additional\_contacts](#input\_additional\_contacts) | List of map where would be the contacts for BILLING, OPERATIONS, SECURITY | `list(map(string))` | n/a | yes |
| <a name="input_admin_role_sandbox"></a> [admin\_role\_sandbox](#input\_admin\_role\_sandbox) | Name of Calebe user in Sandbox account to grant access to ECR in Shared Account | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | proyect environment, user ct for control tower configurations | `string` | n/a | yes |
| <a name="input_iacgroup"></a> [iacgroup](#input\_iacgroup) | owner of the AWS resource | `string` | `"UnAssign"` | no |
| <a name="input_management_aws_organization_id"></a> [management\_aws\_organization\_id](#input\_management\_aws\_organization\_id) | ID of the management organization | `string` | n/a | yes |
| <a name="input_name_sns_event_bucket"></a> [name\_sns\_event\_bucket](#input\_name\_sns\_event\_bucket) | Name of the SNS for registering events buckets | `string` | n/a | yes |
| <a name="input_owner"></a> [owner](#input\_owner) | owner of the AWS resource | `string` | `"IT"` | no |
| <a name="input_prefix"></a> [prefix](#input\_prefix) | Prefix that is always at the beginning of the bucket name  and other components | `string` | `""` | no |
| <a name="input_region"></a> [region](#input\_region) | aws region | `string` | n/a | yes |
| <a name="input_sns_endpoint"></a> [sns\_endpoint](#input\_sns\_endpoint) | Value of the endpoint | `list(string)` | n/a | yes |
| <a name="input_sns_protocol"></a> [sns\_protocol](#input\_sns\_protocol) | Protocol for the sns | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_printouts_roles"></a> [printouts\_roles](#output\_printouts\_roles) | n/a |

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.5 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.45.0 |
| <a name="provider_terraform"></a> [terraform](#provider\_terraform) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_dl-account-p"></a> [dl-account-p](#module\_dl-account-p) | ../modules/L1/ecr | n/a |
| <a name="module_dl-consumers"></a> [dl-consumers](#module\_dl-consumers) | ../modules/L1/ecr | n/a |
| <a name="module_dl-customer-p"></a> [dl-customer-p](#module\_dl-customer-p) | ../modules/L1/ecr | n/a |
| <a name="module_dl-posting-p"></a> [dl-posting-p](#module\_dl-posting-p) | ../modules/L1/ecr | n/a |
| <a name="module_global-reconciliator-api"></a> [global-reconciliator-api](#module\_global-reconciliator-api) | ../modules/L1/ecr | n/a |
| <a name="module_kms_secrets"></a> [kms\_secrets](#module\_kms\_secrets) | ../modules/L1/kms | n/a |
| <a name="module_reconciliator-api"></a> [reconciliator-api](#module\_reconciliator-api) | ../modules/L1/ecr | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_availability_zones.available](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/availability_zones) | data source |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_vpc.networking_vpc](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/vpc) | data source |
| [terraform_remote_state.infra](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cluster_version"></a> [cluster\_version](#input\_cluster\_version) | Kubernetes cluster version | `string` | `"1.29"` | no |
| <a name="input_eks_cluster_name"></a> [eks\_cluster\_name](#input\_eks\_cluster\_name) | EKS Cluster name | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | proyect environment, user ct for control tower configurations | `string` | n/a | yes |
| <a name="input_iacgroup"></a> [iacgroup](#input\_iacgroup) | owner of the AWS resource | `string` | `"UnAssign"` | no |
| <a name="input_intra_subnets"></a> [intra\_subnets](#input\_intra\_subnets) | A list of public subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_owner"></a> [owner](#input\_owner) | owner of the AWS resource | `string` | `"IT"` | no |
| <a name="input_prefix"></a> [prefix](#input\_prefix) | Prefix that is always at the beginning of the bucket name  and other components | `string` | `""` | no |
| <a name="input_private_subnets"></a> [private\_subnets](#input\_private\_subnets) | A list of private subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_private_subnets_id"></a> [private\_subnets\_id](#input\_private\_subnets\_id) | A list of private subnets id inside the VPC | `list(string)` | `[]` | no |
| <a name="input_public_subnets"></a> [public\_subnets](#input\_public\_subnets) | A list of public subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_region"></a> [region](#input\_region) | aws region | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_eks_init"></a> [eks\_init](#output\_eks\_init) | Run the following command to connect to the EKS cluster. |
<!-- END_TF_DOCS -->