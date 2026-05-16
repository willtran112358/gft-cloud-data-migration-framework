variable "environment" {
  type        = string
  description = "Environment"
}

variable "component" {
  type        = string
  description = "Component"
}

variable "context" {
  type        = string
  description = "Context"
  default     = ""
}

variable "region" {
  type        = string
  description = "aws region"
  default     = "eu-central-1"
}

variable "prefix" {
  type        = string
  description = "Prefix that is always at the beginning of the bucket name"
  default     = ""
}

variable "kms_key_arn" {
  type        = string
  description = "KMS key's ARN for encryption of the bucket"
}

variable "extended_policy_json" {
  type        = string
  description = "S3 bucket policy to be merged with the default one"
  default     = ""
}

variable "enable_versioning" {
  type        = bool
  description = "Enabled/Disabled versioning"
  default     = true
}

variable "object_lock_enabled" {
  type        = bool
  description = "Enabled/Disabled object lock configuration"
  default     = true
}

variable "noncurrent_days" {
  type        = number
  description = "nonconcurrent days for retention files in bucket"
  default     = 365
}

variable "expiration_days" {
  type        = number
  description = "expiration days for retention files in bucket"
  default     = 365
}

variable "s3-access-logs" {
  type        = string
  description = "log archive s3 central access-logs"
  default     = ""
}

variable "sns_event_bucket_arn" {
  type        = string
  description = "The arn of the sns topic to attach for the access events"
}