#policy for Flowlog Bucket
data "aws_iam_policy_document" "s3-flowlogs-policy" {
  statement {
    sid       = "AWSLogDeliveryWrite"
    effect    = "Allow"
    resources = ["${module.s3_flowlogs.bucket_arn}/*"]
    actions   = ["s3:PutObject"]

    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }

    principals {
      type        = "Service"
      identifiers = ["delivery.logs.amazonaws.com"]
    }
  }

  statement {
    sid       = "AWSLogDeliveryCheck"
    effect    = "Allow"
    resources = ["${module.s3_flowlogs.bucket_arn}"]
    actions   = ["s3:GetBucketAcl"]

    principals {
      type        = "Service"
      identifiers = ["delivery.logs.amazonaws.com"]
    }
  }

  statement {
    sid    = "DenyUnencryptedTraffic"
    effect = "Deny"

    resources = [
      "${module.s3_flowlogs.bucket_arn}/*",
      "${module.s3_flowlogs.bucket_arn}",
    ]

    actions = ["s3:*"]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}

#policy for Access-loging Bucket
data "aws_iam_policy_document" "s3-access-logs-policy" {

  statement {
    sid       = "S3PolicyStmt-DO-NOT-MODIFY-1700751320588"
    effect    = "Allow"
    resources = ["${module.s3_access_logs.bucket_arn}/*"]

    actions = ["s3:PutObject"]

    principals {
      type        = "Service"
      identifiers = ["logging.s3.amazonaws.com"]
    }

  }
}

data "aws_iam_policy_document" "sns_assume_policy" {
  statement {
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "Service"
      identifiers = ["sns.amazonaws.com"]
    }
  }

}

data "aws_iam_policy_document" "topic" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }

    actions = ["sns:Publish"]
    #resources = ["arn:aws:sns:eu-central-1:724757278519:sns_event_bucket"]
    resources = ["arn:aws:sns:*:*:*"]

    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:s3:*:*:*"]
    }
  }
}

data "aws_iam_policy_document" "sns_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:PutMetricFilter",
      "logs:PutRetentionPolicy"
    ]
    resources = ["*"]
  }
}
