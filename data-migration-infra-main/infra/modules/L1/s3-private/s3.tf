resource "aws_s3_bucket" "this" {
  #checkov:skip=CKV_AWS_144: "Ensure that S3 bucket has cross-region replication enabled"
  #checkov:skip=CKV_AWS_18: "Ensure the S3 bucket has access logging enabled"
  #checkov:skip=CKV_AWS_19: "Ensure all data stored in the S3 bucket is securely encrypted at rest"
  #checkov:skip=CKV_AWS_145: "Ensure that S3 buckets are encrypted with KMS by default"
  #checkov:skip=CKV_AWS_21: "Ensure all data stored in the S3 bucket have versioning enabled"
  bucket              = "${lower(local.account_id)}-${lower(var.region)}-${lower(var.prefix)}-${lower(var.environment)}-${lower(var.component)}"
  object_lock_enabled = var.object_lock_enabled
}

# resource "aws_s3_bucket_logging" "example" {
#   count  = var.s3-access-logs != "" ? 1 : 0
#   bucket = aws_s3_bucket.this.id

#   target_bucket = var.s3-access-logs
#   target_prefix = "${lower(var.component)}/"
# }

resource "aws_s3_bucket_ownership_controls" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  count = var.kms_key_arn != "" ? 1 : 0

  bucket = aws_s3_bucket.this.bucket

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = var.kms_key_arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_object_lock_configuration" "this" {
  count = var.object_lock_enabled ? 1 : 0

  bucket = aws_s3_bucket.this.bucket
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.bucket

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Disabled"
  }
}

resource "aws_s3_bucket_acl" "this" {
  bucket = aws_s3_bucket.this.id
  acl    = "private"

  depends_on = [aws_s3_bucket_ownership_controls.this]
}

resource "aws_s3_bucket_public_access_block" "deny_access_public" {
  bucket                  = aws_s3_bucket.this.id
  block_public_acls       = true
  block_public_policy     = true
  restrict_public_buckets = true
  ignore_public_acls      = true
}

resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.this.id

  rule {
    id     = "retention"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = var.noncurrent_days
    }

    expiration {
      days = var.expiration_days
    }
  }
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.this.id

  topic {
    topic_arn = var.sns_event_bucket_arn
    events    = ["s3:ObjectRemoved:Delete", "s3:LifecycleExpiration:Delete", "s3:LifecycleExpiration:DeleteMarkerCreated"]
  }
}