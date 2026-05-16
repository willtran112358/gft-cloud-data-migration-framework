variable "belong" {
  description = "primary key which secret manager belong"
  type        = string
}

variable "secret_name" {
  description = "Secret name for vault core database user"
  type        = string
}

variable "secret_kms_key_id" {
  description = "ARN or Id of the AWS KMS key to be used to encrypt the secret values in the versions stored in this secret."
  type        = string
  default     = "aws/secretsmanager"
}

variable "secret_recovery_window_in_days" {
  description = "Number of days that AWS Secrets Manager waits before it can delete the secret. This value can be 0 to force deletion without recovery or range from 7 to 30 days."
  default     = 30
  type        = number
}

variable "secret_name_prefix" {
  description = "Creates a unique name beginning with the specified prefix. Conflicts with name."
  default     = null
  type        = string
}

variable "secret_replica" {
  description = "Configuration block to support secret replication. See details below."
  type = list(object({
    kms_key_id = string
    region     = string
  }))
  default = []
}

variable "secret_string" {
  description = "The json secret values is endcoded to string"
  type        = map(any)
  default     = {}
}

variable "create_password" {
  description = "This is boolean that is true will create random password or false not create."
  type        = bool
  default     = false
}

variable "force_overwrite_replica_secret" {
  description = "Accepts boolean value to specify whether to overwrite a secret with the same name in the destination Region."
  type        = bool
  default     = false
}

variable "iam_policies" {
  description = "IAM policy details"
  type = list(object({
    sid    = string
    effect = string
    principals = object({
      type        = string
      identifiers = list(string)
    })
    actions   = list(string)
  }))
  default = []
}

# variable "database_enpoint" {
#   description = "Master database enpoint of vault core"
#   type        = string
# }

variable "env_tags" {
  type        = map(string)
  description = "Environment tags configured for all provisioned resources"
}

variable "global_tags" {
  type        = map(string)
  description = "Global tags configured for all provisioned resources"
}

