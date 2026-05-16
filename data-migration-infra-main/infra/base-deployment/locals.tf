data "aws_caller_identity" "current" {}
# data "aws_availability_zones" "available" {}

# data "terraform_remote_state" "infra" {
#   backend = "s3"
#   config = {
#     bucket = "${var.aws_account}-${var.region}-terraform-state"
#     key    = "development/infra/networking/terraform.tfstate"
#     region = "${var.region}"
#   }
# }

# data "aws_vpc" "networking_vpc" {
#   filter {
#     name   = "tag:Name"
#     values = ["networking-vpc*"]
#   }
# }

# data "aws_kms_key" "by_alias" {
#   key_id = "aws/secretsmanager"
# }

# locals {
#   account_id          = data.aws_caller_identity.current.account_id
#   azs                 = slice(data.aws_availability_zones.available.names, 0, 3)
#   vpc_id              = data.aws_vpc.networking_vpc.id
#   vpc_cidr            = data.aws_vpc.networking_vpc.cidr_block
#   public_subnets_ids  = data.terraform_remote_state.infra.outputs.public_subnets_id
#   private_subnets_ids = data.terraform_remote_state.infra.outputs.private_subnets_id
#   #kms_secret_manager = data.aws_kms_key.by_alias.arn
# }
