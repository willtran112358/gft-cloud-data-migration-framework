variable "name" {
  type        = string
  description = "Name of the Cloudtrail"
}

variable "s3_bucket_name" {
  type        = string
  description = "Name of the S3 to attach"
}

variable "s3_key_prefix" {
  type        = string
  description = "S3 key prefix"
}