data "aws_caller_identity" "current" {}
# data "aws_availability_zones" "available" {}

# data "aws_vpc" "networking_vpc" {
#   filter {
#     name   = "tag:Name"
#     values = ["networking-vpc"] # insert values here
#   }
# }

# data "aws_subnets" "private_subnets" {
#   filter {
#     name   = "tag:Name"
#     values = ["networking-vpc-private-eu-central-1a", "networking-vpc-private-eu-central-1b"] # insert values here
#   }
# }

# data "aws_subnets" "public_subnets" {
#   filter {
#     name   = "tag:Name"
#     values = ["networking-vpc-public-eu-central-1a", "networking-vpc-public-eu-central-1b"] # insert values here
#   }
# }
# data "aws_kms_key" "by_alias" {
#   key_id = "aws/secretsmanager"
# }

locals {
  # account_id          = data.aws_caller_identity.current.account_id
  # azs                 = slice(data.aws_availability_zones.available.names, 0, 3)
  vpc_id = "vpc-0962cb9f6bcc7a99a"
  # vpc_cidr            = data.aws_vpc.networking_vpc.cidr_block
  public_subnets_ids  = ["subnet-003242a8defe1c019", "subnet-0bb4ad82d014744e7"]
  private_subnets_ids = ["subnet-058b30ddd6e68b54b", "subnet-03d06e9e10bf8f262"]
  #kms_secret_manager = data.aws_kms_key.by_alias.arn
  # kms_lambda_arn = data.aws_kms_key.kms_lambda.arn
}

# data "aws_kms_key" "kms_lambda" {
#   key_id = "alias/lambda"
# }