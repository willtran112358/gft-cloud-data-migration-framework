resource "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/python/lambda_function.py"
  output_path = "${path.module}/python/lambda_function.zip"
}

resource "aws_lambda_function" "create_namespace_lambda" {
  filename         = archive_file.lambda_zip.output_path
  function_name    = "create-k8s-namespace"
  description      = "create a namespace on EKS cluster"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  timeout          = 180
  source_code_hash = archive_file.lambda_zip.output_base64sha256
  tracing_config {
    mode = "Active"
  }

  vpc_config {
    subnet_ids         = local.private_subnets_ids
    security_group_ids = [module.lambdas_security_group.security_group_id]
  }

  environment {
    variables = {
      CLUSTER_NAME = "${var.cluster_prefix}-${var.eks_cluster_name}"
      REGION       = var.region
      NAMESPACE    = var.cluster_namespace
    }
  }
  kms_key_arn = ""
}

resource "null_resource" "invoke_lambda" {
  provisioner "local-exec" {
    command = <<EOT
      aws lambda invoke --region ${var.region} --function-name ${aws_lambda_function.create_namespace_lambda.function_name} output.json
    EOT
  }
}

# resource "aws_iam_role" "lambda_role" {
#   name               = "lambda-lambdaRole-waf"
#   # assume_role_policy = data.aws_iam_policy_document.s3-access-logs-policy.json
#   # assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
#   assume_role_policy = data.aws_iam_policy_document.lambda_permissions.json
# }
resource "aws_iam_role" "lambda_role" {
  name               = "lambda-lambdaRole-waf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}
resource "aws_iam_role_policy" "lambda_permissions_policy" {
  name   = "lambda-network-access"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.lambda_permissions.json
}
resource "aws_iam_role_policy_attachment" "lambda_permissions_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.iam_policy.arn
}
resource "aws_iam_policy" "iam_policy" {
  name        = "lambda-network-access"
  description = "IAM policy for lambda to access network resources"
  policy      = data.aws_iam_policy_document.lambda_permissions.json
}