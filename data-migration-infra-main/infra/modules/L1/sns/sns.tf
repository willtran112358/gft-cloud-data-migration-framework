resource "aws_sns_topic" "this" {
  name                                = var.name
  kms_master_key_id                   = var.kms_master_key_id
  lambda_success_feedback_role_arn    = var.lambda_success_feedback_role_arn
  lambda_success_feedback_sample_rate = var.lambda_success_feedback_sample_rate
  lambda_failure_feedback_role_arn    = var.lambda_failure_feedback_role_arn
  policy                              = var.policy_topic
}

resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
  #count = var.endpoint != "" ? 1 : 0
  count = length(var.endpoint)

  topic_arn = aws_sns_topic.this.arn
  protocol  = var.protocol
  endpoint  = var.endpoint[count.index]

}