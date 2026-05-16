module "s3_source_files" {
  source               = "../modules/L1/s3-private"
  kms_key_arn          = ""
  environment          = var.environment
  region               = var.region
  component            = "raw"
  prefix               = var.prefix
  sns_event_bucket_arn = var.sns_event_arn
  object_lock_enabled  = false
}

resource "aws_s3_object" "s3_source_files_dirs" {
  for_each = var.s3_source_files_dirs
  bucket   = module.s3_source_files.bucket_id
  key      = "${each.value}/"
}

module "s3_raw" {
  source               = "../modules/L1/s3-private"
  kms_key_arn          = ""
  environment          = var.environment
  region               = var.region
  component            = "raw"
  prefix               = var.prefix
  sns_event_bucket_arn = var.sns_event_arn
}

module "s3_staging" {
  source               = "../modules/L1/s3-private"
  kms_key_arn          = ""
  environment          = var.environment
  region               = var.region
  component            = "staging"
  prefix               = var.prefix
  sns_event_bucket_arn = var.sns_event_arn
}

module "s3_migration" {
  source               = "../modules/L1/s3-private"
  kms_key_arn          = ""
  environment          = var.environment
  region               = var.region
  component            = "migration"
  prefix               = var.prefix
  sns_event_bucket_arn = var.sns_event_arn
}

module "s3_athena_queries" {
  source               = "../modules/L1/s3-private"
  kms_key_arn          = ""
  environment          = var.environment
  region               = var.region
  component            = "athena-queries"
  prefix               = var.prefix
  sns_event_bucket_arn = var.sns_event_arn
}
