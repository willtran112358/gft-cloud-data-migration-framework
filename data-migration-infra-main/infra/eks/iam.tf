data "aws_iam_policy_document" "s3-access-logs-policy" {
  statement {
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole"
    ]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda_permissions" {
  statement {
    effect = "Allow"
    actions = [
      "ec2:*",
      "eks:*",
      "iam:PassRole",
      "lambda:InvokeFunction",
      "logs:*",
      "s3:*",
      "sns:*",
      "cloudwatch:*"
    ]
    resources = ["*"]
  }
}
