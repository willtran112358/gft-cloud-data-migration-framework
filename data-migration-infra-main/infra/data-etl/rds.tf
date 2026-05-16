#############################################################
#### AWS Secret Manager
#############################################################
module "secret_manager" {
  source                         = "../modules/HDBank/secret_manager"

  for_each                       = { for _, v in var.secret_managers : v.secret_name => v }
  create_password                = each.value.create_password
  secret_name                    = each.value.secret_name
  belong                         = each.value.belong
  iam_policies                   = lookup(each.value, "iam_policies", [])
  secret_kms_key_id              = lookup(each.value, "secret_kms_key_id", null)
  secret_name_prefix             = lookup(each.value, "secret_name_prefix", null)
  secret_recovery_window_in_days = lookup(each.value, "secret_recovery_window_in_days", 30)
  force_overwrite_replica_secret = lookup(each.value, "force_overwrite_replica_secret", false)
  secret_replica                 = lookup(each.value, "secret_replica", [])
  secret_string                  = lookup(each.value, "secret_string", null)
  env_tags                       = var.env_tags
  global_tags                    = var.global_tags
}

locals {
  temp = toset([for k, v in module.secret_manager : v.belong])
  msk_secret_manager = {
    for _, belong in local.temp : belong => [
      for k, v in module.secret_manager : v.aws_secretsmanager_secret.arn if v.belong == var.msk_primary_key
    ]
  }
}

############################################################
### RDS AURORA POSTGRESQL
############################################################
module "rds" {
  source = "../modules/HDBank/rds"
  use_aurora = false

  vpc_id                       = var.vpc_id
  cidr_range                   = var.rds_cidr_range
  name                         = var.db_name
  family                       = var.db_family
  postgres_version             = var.db_version
  username                     = var.db_username
  password                     = module.secret_manager[var.db_secret_manager].password
  storage_type                 = var.db_storage_type
  instance_class               = var.db_instance_class
  allocated_storage            = var.db_allocated_storage
  max_allocated_storage        = var.db_max_allocated_storage
  db_subnet_group              = var.db_subnet_group
  multi_az                     = var.db_multi_az
  deletion_protection          = var.db_deletion_protection
  performance_insights_enabled = var.db_performance_insights_enabled
  backup_window                = var.db_backup_window
  backup_retention_period      = var.db_backup_retention_period
  maintenance_window           = var.db_maintenance_window
  parameter                    = var.db_parameter_group
  db_record_name               = var.db_record_name
  env_tags                     = var.env_tags
  tags                         = var.global_tags

  environment = var.environment
  project = var.project
  depends_on = [module.secret_manager]

}
############################################################