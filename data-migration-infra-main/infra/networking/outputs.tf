# output "private_subnets_id" {
#   value = module.vpc_with_flow_logs_cloudwatch_logs_default.private_subnets
# }

# output "intra_subnets_id" {
#   value = module.vpc_with_flow_logs_cloudwatch_logs_default.intra_subnets
# }

# output "public_subnets_id" {
#   value = module.vpc_with_flow_logs_cloudwatch_logs_default.public_subnets
# }

# output "vpc_id" {
#   value = module.vpc_with_flow_logs_cloudwatch_logs_default.vpc_id
# }

output "kms_lambda_arn" {
  value = module.kms_lambda.kms_key_arn
}