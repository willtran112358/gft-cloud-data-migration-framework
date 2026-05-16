################################################################################
# data Migration ECR Repository
################################################################################
module "dl-customer-p" {
  source = "../modules/L1/ecr"

  repository_name = "dl-customer-p"
  # repository_encryption_type      = "KMS"
  repository_image_tag_mutability   = "MUTABLE"
  # repository_read_write_access_arns = ["arn:aws:iam::${var.aws_account}:role/aws-reserved/sso.amazonaws.com/eu-west-2/${var.federated_user}", data.aws_caller_identity.current.arn]
  repository_read_write_access_arns = ["*"]

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "delete untagged images",
        selection = {
          tagStatus = "untagged",
          countType = "sinceImagePushed",
          countUnit : "days",
          countNumber = 1
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

module "dl-account-p" {
  source = "../modules/L1/ecr"

  repository_name = "dl-account-p"
  # repository_encryption_type      = "KMS"
  repository_image_tag_mutability   = "MUTABLE"
  # repository_read_write_access_arns = ["arn:aws:iam::${var.aws_account}:role/aws-reserved/sso.amazonaws.com/eu-west-2/${var.federated_user}", data.aws_caller_identity.current.arn]
  repository_read_write_access_arns = ["*"]

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "delete untagged images",
        selection = {
          tagStatus = "untagged",
          countType = "sinceImagePushed",
          countUnit : "days",
          countNumber = 1
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

module "dl-posting-p" {
  source = "../modules/L1/ecr"

  repository_name = "dl-posting-p"
  # repository_encryption_type      = "KMS"
  repository_image_tag_mutability   = "MUTABLE"
  # repository_read_write_access_arns = ["arn:aws:iam::${var.aws_account}:role/aws-reserved/sso.amazonaws.com/eu-west-2/${var.federated_user}", data.aws_caller_identity.current.arn]
  repository_read_write_access_arns = ["*"]

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "delete untagged images",
        selection = {
          tagStatus = "untagged",
          countType = "sinceImagePushed",
          countUnit : "days",
          countNumber = 1
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

module "dl-consumers" {
  source = "../modules/L1/ecr"

  repository_name = "dl-consumers"
  # repository_encryption_type      = "KMS"
  repository_image_tag_mutability   = "MUTABLE"
  # repository_read_write_access_arns = ["arn:aws:iam::${var.aws_account}:role/aws-reserved/sso.amazonaws.com/eu-west-2/${var.federated_user}", data.aws_caller_identity.current.arn]
  repository_read_write_access_arns = ["*"]

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "delete untagged images",
        selection = {
          tagStatus = "untagged",
          countType = "sinceImagePushed",
          countUnit : "days",
          countNumber = 1
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

module "reconciliator-api" {
  source = "../modules/L1/ecr"

  repository_name = "reconciliator-api"
  # repository_encryption_type      = "KMS"
  repository_image_tag_mutability   = "MUTABLE"
  # repository_read_write_access_arns = ["arn:aws:iam::${var.aws_account}:role/aws-reserved/sso.amazonaws.com/eu-west-2/${var.federated_user}", data.aws_caller_identity.current.arn]
  repository_read_write_access_arns = ["*"]

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "delete untagged images",
        selection = {
          tagStatus = "untagged",
          countType = "sinceImagePushed",
          countUnit : "days",
          countNumber = 1
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

module "global-reconciliator-api" {
  source = "../modules/L1/ecr"

  repository_name = "global-reconciliator-api"
  # repository_encryption_type      = "KMS"
  repository_image_tag_mutability = "MUTABLE"
  # repository_read_write_access_arns = ["arn:aws:iam::${var.aws_account}:role/aws-reserved/sso.amazonaws.com/eu-west-2/${var.federated_user}",
  # "arn:aws:iam::${var.aws_account}:user/s-aws-data-migration-accelerator-DEV", data.aws_caller_identity.current.arn]
  repository_read_write_access_arns = ["*"]

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "delete untagged images",
        selection = {
          tagStatus = "untagged",
          countType = "sinceImagePushed",
          countUnit : "days",
          countNumber = 1
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}
