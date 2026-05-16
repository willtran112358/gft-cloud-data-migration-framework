module "sns_role" {
  source = "../modules/L1/iam-role"

  iam_policy_name    = "${var.prefix}-sns_policy"
  policy             = data.aws_iam_policy_document.sns_policy.json
  name               = "${var.prefix}-sns_role"
  assume_role_policy = data.aws_iam_policy_document.sns_assume_policy.json

}