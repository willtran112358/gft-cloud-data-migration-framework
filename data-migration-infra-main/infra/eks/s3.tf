module "s3_k8s_deployments" {
  source               = "../modules/L1/s3-private"
  kms_key_arn          = ""
  environment          = var.environment
  region               = var.region
  component            = "k8s-deployments"
  prefix               = var.prefix
  # extended_policy_json = data.aws_iam_policy_document.s3-access-logs-policy.json
  sns_event_bucket_arn = var.sns_event_arn
  object_lock_enabled  = false
}
resource "aws_s3_object" "consumers_folder" {
  bucket = module.s3_k8s_deployments.bucket_id
  key    = "consumers/"
}

resource "aws_s3_object" "producer_folder" {
  bucket = module.s3_k8s_deployments.bucket_id
  key    = "producers/"
}