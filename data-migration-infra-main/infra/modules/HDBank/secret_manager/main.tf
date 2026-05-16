resource "random_string" "random_password" {
  count   = var.create_password ? 1 : 0
  length  = 32
  special = false
}

data "aws_kms_key" "this" {
  count = var.secret_kms_key_id != null && var.secret_kms_key_id != "" ? 1 : 0
  key_id = var.secret_kms_key_id
}

locals {
  kms_key_id = length(data.aws_kms_key.this) > 0 ? data.aws_kms_key.this[0].id : ""
}

resource "aws_secretsmanager_secret" "this" {
  name                    = var.secret_name
  kms_key_id              = local.kms_key_id
  name_prefix             = local.name_prefix
  recovery_window_in_days = local.recovery_window_in_days
  dynamic "replica" {
    for_each = local.replica
    content {
      kms_key_id = replica.value.kms_key_id
      region     = replica.value.region
    }
  }

  force_overwrite_replica_secret = local.force_overwrite_replica_secret
  tags                           = local.tags
  description                    = "Credentials specific user for setup database of Vault Core"
}

resource "aws_secretsmanager_secret_version" "data" {
  count     = var.create_password ? 0 : 1
  secret_id = aws_secretsmanager_secret.this.id

  #   secret_string = jsonencode({
  #     "${var.database_enpoint}" : "${random_string.random_password.result}"
  #   })
  secret_string = jsonencode(var.secret_string)
  lifecycle {
    ignore_changes = [
      secret_string
    ]
  }
}

resource "aws_secretsmanager_secret_version" "data_with_password" {
  count     = var.create_password ? 1 : 0
  secret_id = aws_secretsmanager_secret.this.id

  secret_string = jsonencode(merge(var.secret_string, {
    "password" : "${random_string.random_password[0].result}"
  }))

  lifecycle {
    ignore_changes = [
      secret_string
    ]
  }
}

data "aws_iam_policy_document" "this" {
  count = local.create_policy ? 1 : 0
  dynamic "statement" {
    for_each = var.iam_policies
    content {
      sid    = statement.value.sid
      effect = statement.value.effect
      principals {
        type        = statement.value.principals.type
        identifiers = statement.value.principals.identifiers
      }
      actions   = statement.value.actions
      resources = [aws_secretsmanager_secret.this.arn]
    }
  }
}

resource "aws_secretsmanager_secret_policy" "this" {
  count      = local.create_policy ? 1 : 0
  secret_arn = aws_secretsmanager_secret.this.arn
  policy     = data.aws_iam_policy_document.this[0].json
}
