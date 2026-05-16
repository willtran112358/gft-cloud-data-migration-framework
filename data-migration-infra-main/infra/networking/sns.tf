module "sns_event_buckets" {
  source = "../modules/L1/sns"

  name                                = "${var.prefix}-${var.name_sns_event_bucket}"
  protocol                            = var.sns_protocol
  endpoint                            = var.sns_endpoint
  kms_master_key_id                   = "alias/aws/sns"
  lambda_success_feedback_role_arn    = module.sns_role.iam_role_arn
  lambda_failure_feedback_role_arn    = module.sns_role.iam_role_arn
  lambda_success_feedback_sample_rate = "100"
  policy_topic                        = data.aws_iam_policy_document.topic.json

}