data "aws_caller_identity" "current" {}

module "kms_cloudwatch" {
  source = "../../L1/kms"

  service_name = "cloudwatch"

  service_principals_with_general_conditions = [
    {
      svc_identifiers = ["logs.${var.region}.amazonaws.com"]
      condition = [
        {
          test     = "ArnEquals"
          values   = ["arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:*"]
          variable = "kms:EncryptionContext:aws:logs:arn"
        }
      ]
    }
  ]
}
