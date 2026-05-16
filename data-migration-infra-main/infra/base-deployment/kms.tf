module "kms_secrets" {
  source                  = "../modules/L1/kms"
  service_name            = "secretsmanager"
  enable_cloudwatch_alarm = true
  enable_key_rotation     = true
  services_principal      = ["secretsmanager.amazonaws.com"]
}

# resource "aws_kms_key" "eks_ebs" {
#   description = "KMS Key for administrators"
#   policy = jsonencode({
#     "Version" : "2012-10-17",
#     "Id" : "KMS-Key-Policy-For-Admin",
#     "Statement" : [
#       {
#         "Sid" : "Allow access for Key Administrators",
#         "Effect" : "Allow",
#         "Principal" : {
#           "AWS" : "arn:aws:iam::${local.account_id}:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling"
#         },
#         "Action" : [
#             "kms:Encrypt",
#             "kms:Decrypt",
#             "kms:ReEncrypt*",
#             "kms:GenerateDataKey*",
#             "kms:DescribeKey"
#         ],
#         "Resource" : "*"
#       },
#       {
#             "Sid": "Default",
#             "Effect": "Allow",
#             "Principal": {
#                 "AWS": "arn:aws:iam::${local.account_id}:root"
#             },
#             "Action": "kms:*",
#             "Resource": "*"
#         }
#     ],
#     }
#   )
# }

