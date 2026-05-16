resource "aws_cloudtrail" "example" {
  depends_on = [aws_s3_bucket_policy.example]

  name                          = var.name
  s3_bucket_name                = var.s3_bucket_name
  s3_key_prefix                 = var.s3_key_prefix
  include_global_service_events = false
}
