module "s3_access_logs" {
  source = "../modules/L1/s3-private"
  #kms_key_arn    = module.kms_config.kms_key_arn
  kms_key_arn          = ""
  environment          = var.environment
  region               = var.region
  component            = "access-logs"
  prefix               = var.prefix
  extended_policy_json = data.aws_iam_policy_document.s3-access-logs-policy.json
  sns_event_bucket_arn = module.sns_event_buckets.sns_arn
  object_lock_enabled  = false
}

module "s3_flowlogs" {
  source = "../modules/L1/s3-private"
  #kms_key_arn    = module.kms_config.kms_key_arn
  kms_key_arn    = ""
  s3-access-logs = module.s3_access_logs.bucket_domain_name

  environment          = var.environment
  region               = var.region
  component            = "flowlogs"
  prefix               = var.prefix
  extended_policy_json = data.aws_iam_policy_document.s3-flowlogs-policy.json
  sns_event_bucket_arn = module.sns_event_buckets.sns_arn
}