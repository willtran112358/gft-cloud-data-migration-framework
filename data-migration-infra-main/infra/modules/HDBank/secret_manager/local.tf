locals {
  name_prefix                    = can(var.secret_name_prefix) ? var.secret_name_prefix : null
  recovery_window_in_days        = var.secret_recovery_window_in_days
  create_policy                  = length(var.iam_policies) > 0
  replica                        = can(var.secret_replica) ? var.secret_replica : []
  force_overwrite_replica_secret = var.force_overwrite_replica_secret
  tags                           = merge(var.env_tags, var.global_tags)
}
