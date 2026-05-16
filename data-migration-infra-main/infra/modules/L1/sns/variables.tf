variable "name" {
  type        = string
  description = "Name of the sns"
}

variable "kms_master_key_id" {
  type        = string
  description = "KMS cypher for sns"
}

variable "lambda_success_feedback_role_arn" {
  type        = string
  description = "SNS role arn for lambda success"
  default     = ""
}

variable "lambda_success_feedback_sample_rate" {
  type        = string
  description = "Percentage of success rate for lambda logs"
  default     = null
}

variable "lambda_failure_feedback_role_arn" {
  type        = string
  description = "SNS role arn for lambda failure"
  default     = ""
}

variable "protocol" {
  type        = string
  description = " Protocol for the sns"
}

variable "endpoint" {
  type        = list(string)
  description = "List of emails attached to the topic"
}

variable "policy_topic" {
  type        = string
  description = "value"
}