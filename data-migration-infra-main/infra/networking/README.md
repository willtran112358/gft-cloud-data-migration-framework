## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 5.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_kms"></a> [kms](#module\_kms) | ../modules/L2/kms-networking | n/a |
| <a name="module_vpc_endpoints"></a> [vpc\_endpoints](#module\_vpc\_endpoints) | ../modules/L2/vpc/modules/vpc-endpoints | n/a |
| <a name="module_vpc_endpoints_security_group"></a> [vpc\_endpoints\_security\_group](#module\_vpc\_endpoints\_security\_group) | ../modules/L2/security-group | n/a |
| <a name="module_vpc_with_flow_logs_cloudwatch_logs_default"></a> [vpc\_with\_flow\_logs\_cloudwatch\_logs\_default](#module\_vpc\_with\_flow\_logs\_cloudwatch\_logs\_default) | ../modules/L2/vpc | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_ec2_transit_gateway_vpc_attachment.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ec2_transit_gateway_vpc_attachment) | resource |
| [aws_eip.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eip) | resource |
| [aws_flow_log.s3_flow_logs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/flow_log) | resource |
| [aws_iam_policy.vpc_flow_log_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.vpc_flow_log_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.vpc_flow_log_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_route.internet-all](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | resource |
| [aws_route.local](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | resource |
| [aws_route.tgw_routes](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | resource |
| [aws_route.vpn_basikon_host](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | resource |
| [aws_route.vpn_honda_it](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | resource |
| [aws_vpc_endpoint.ec2](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_endpoint) | resource |
| [aws_availability_zones.available](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/availability_zones) | data source |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.flow_log_cloudwatch_assume_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.vpc_flow_log_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_account_name"></a> [account\_name](#input\_account\_name) | aws account name | `string` | n/a | yes |
| <a name="input_component"></a> [component](#input\_component) | Component | `string` | n/a | yes |
| <a name="input_elastic_ip_identifiers"></a> [elastic\_ip\_identifiers](#input\_elastic\_ip\_identifiers) | List of eip identifiers | `list(string)` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | environment | `string` | n/a | yes |
| <a name="input_flowlogs_bucket"></a> [flowlogs\_bucket](#input\_flowlogs\_bucket) | flowlogs bucket in log archive account | `string` | `""` | no |
| <a name="input_iacgroup"></a> [iacgroup](#input\_iacgroup) | owner of the AWS resource | `string` | `"UnAssign"` | no |
| <a name="input_on-premise-cidr"></a> [on-premise-cidr](#input\_on-premise-cidr) | on premise CIDR netwrok | `string` | n/a | yes |
| <a name="input_owner"></a> [owner](#input\_owner) | owner of the AWS resource | `string` | `"IT"` | no |
| <a name="input_prefix"></a> [prefix](#input\_prefix) | Prefix that is always at the beginning of the bucket name | `string` | `""` | no |
| <a name="input_private_subnets"></a> [private\_subnets](#input\_private\_subnets) | A list of private subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_public_subnets"></a> [public\_subnets](#input\_public\_subnets) | A list of public subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_region"></a> [region](#input\_region) | Region in which the resources will be deployed | `string` | n/a | yes |
| <a name="input_tgw_id"></a> [tgw\_id](#input\_tgw\_id) | transit gateway id from networking account | `string` | n/a | yes |
| <a name="input_vpc_cidr"></a> [vpc\_cidr](#input\_vpc\_cidr) | vpc cidr | `string` | `""` | no |
| <a name="input_vpn_basikon_host"></a> [vpn\_basikon\_host](#input\_vpn\_basikon\_host) | Basikon VPN host | `any` | n/a | yes |
| <a name="input_vpn_honda_it_cidr"></a> [vpn\_honda\_it\_cidr](#input\_vpn\_honda\_it\_cidr) | cidr on-premise | `any` | n/a | yes |
| <a name="input_vpn_honda_users_cidr"></a> [vpn\_honda\_users\_cidr](#input\_vpn\_honda\_users\_cidr) | cidr on-premise | `any` | n/a | yes |
| <a name="input_vpn_on_premise_cidr"></a> [vpn\_on\_premise\_cidr](#input\_vpn\_on\_premise\_cidr) | cidr on-premise | `any` | n/a | yes |

## Outputs

No outputs.

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.47.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_athena_endpoints"></a> [athena\_endpoints](#module\_athena\_endpoints) | ../modules/L2/vpc/modules/vpc-endpoints | n/a |
| <a name="module_kms"></a> [kms](#module\_kms) | ../modules/L2/kms-networking | n/a |
| <a name="module_kms_lambda"></a> [kms\_lambda](#module\_kms\_lambda) | ../modules/L1/kms | n/a |
| <a name="module_s3_access_logs"></a> [s3\_access\_logs](#module\_s3\_access\_logs) | ../modules/L1/s3-private | n/a |
| <a name="module_s3_endpoint"></a> [s3\_endpoint](#module\_s3\_endpoint) | ../modules/L2/vpc/modules/vpc-endpoints | n/a |
| <a name="module_s3_flowlogs"></a> [s3\_flowlogs](#module\_s3\_flowlogs) | ../modules/L1/s3-private | n/a |
| <a name="module_sns_event_buckets"></a> [sns\_event\_buckets](#module\_sns\_event\_buckets) | ../modules/L1/sns | n/a |
| <a name="module_sns_role"></a> [sns\_role](#module\_sns\_role) | ../modules/L1/iam-role | n/a |
| <a name="module_vpc_endpoints_security_group"></a> [vpc\_endpoints\_security\_group](#module\_vpc\_endpoints\_security\_group) | ../modules/L2/security-group | n/a |
| <a name="module_vpc_with_flow_logs_cloudwatch_logs_default"></a> [vpc\_with\_flow\_logs\_cloudwatch\_logs\_default](#module\_vpc\_with\_flow\_logs\_cloudwatch\_logs\_default) | ../modules/L2/vpc | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_eip.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eip) | resource |
| [aws_flow_log.s3_flow_logs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/flow_log) | resource |
| [aws_iam_policy.vpc_flow_log_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.vpc_flow_log_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.vpc_flow_log_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_availability_zones.available](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/availability_zones) | data source |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.flow_log_cloudwatch_assume_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.s3-access-logs-policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.s3-flowlogs-policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sns_assume_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sns_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.topic](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.vpc_flow_log_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_component"></a> [component](#input\_component) | Component | `string` | n/a | yes |
| <a name="input_elastic_ip_identifiers"></a> [elastic\_ip\_identifiers](#input\_elastic\_ip\_identifiers) | List of eip identifiers | `list(string)` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | environment | `string` | n/a | yes |
| <a name="input_flowlogs_bucket"></a> [flowlogs\_bucket](#input\_flowlogs\_bucket) | flowlogs bucket in log archive account | `string` | `""` | no |
| <a name="input_iacgroup"></a> [iacgroup](#input\_iacgroup) | owner of the AWS resource | `string` | `"UnAssign"` | no |
| <a name="input_intra_subnets"></a> [intra\_subnets](#input\_intra\_subnets) | A list of public subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_name_sns_event_bucket"></a> [name\_sns\_event\_bucket](#input\_name\_sns\_event\_bucket) | Name of the SNS for registering events buckets | `string` | n/a | yes |
| <a name="input_owner"></a> [owner](#input\_owner) | owner of the AWS resource | `string` | `"IT"` | no |
| <a name="input_prefix"></a> [prefix](#input\_prefix) | Prefix that is always at the beginning of the bucket name | `string` | `""` | no |
| <a name="input_private_subnets"></a> [private\_subnets](#input\_private\_subnets) | A list of private subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_public_subnets"></a> [public\_subnets](#input\_public\_subnets) | A list of public subnets inside the VPC | `list(string)` | `[]` | no |
| <a name="input_region"></a> [region](#input\_region) | Region in which the resources will be deployed | `string` | n/a | yes |
| <a name="input_sns_endpoint"></a> [sns\_endpoint](#input\_sns\_endpoint) | Value of the endpoint | `list(string)` | n/a | yes |
| <a name="input_sns_protocol"></a> [sns\_protocol](#input\_sns\_protocol) | Protocol for the sns | `string` | n/a | yes |
| <a name="input_vpc_cidr"></a> [vpc\_cidr](#input\_vpc\_cidr) | vpc cidr | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_intra_subnets_id"></a> [intra\_subnets\_id](#output\_intra\_subnets\_id) | n/a |
| <a name="output_kms_lambda_arn"></a> [kms\_lambda\_arn](#output\_kms\_lambda\_arn) | n/a |
| <a name="output_private_subnets_id"></a> [private\_subnets\_id](#output\_private\_subnets\_id) | n/a |
| <a name="output_public_subnets_id"></a> [public\_subnets\_id](#output\_public\_subnets\_id) | n/a |
| <a name="output_vpc_id"></a> [vpc\_id](#output\_vpc\_id) | n/a |
<!-- END_TF_DOCS -->