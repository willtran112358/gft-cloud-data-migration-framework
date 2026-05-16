data "aws_caller_identity" "current" {}

data "aws_subnets" "private_subnets" {
  filter {
    name   = "tag:Name"
    values = ["*container*"] # insert values here
  }
}

data "aws_subnets" "public_subnets" {
  filter {
    name   = "tag:Name"
    values = ["*control-plan*"] # insert values here
  }
}

data "aws_eks_cluster" "eks-cluster" {
  # name = "data-migration"
  # HDBank edit
  name = "gft-dm-data-migration"
}

data "aws_vpc" "networking_vpc" {
  filter {
    name   = "tag:Name"
    # values = ["*networking*"]
    values = ["*uat-digital-core*"]
  }
}

data "aws_kms_alias" "cloudwatch" {
  name = "alias/cloudwatch"
}

data "aws_kms_key" "kms_lambda" {
  key_id = "alias/lambda"
}

locals {
  account_id          = data.aws_caller_identity.current.account_id
  vpc_id              = data.aws_vpc.networking_vpc.id
  public_subnets_ids  = data.aws_subnets.public_subnets.ids
  private_subnets_ids = data.aws_subnets.private_subnets.ids
  kms_lambda_arn      = data.aws_kms_key.kms_lambda.arn

}

output "name" {
  value = data.aws_kms_alias.cloudwatch.arn
}
