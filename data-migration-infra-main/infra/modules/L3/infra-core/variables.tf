# Skeleton global variables

variable "environment" {
  type        = string
  description = "Environment, for example sandbox or dev"
}

variable "region" {
  description = "Region"
  type        = string
}

variable "component" {
  type        = string
  default     = "apps"
  description = "Component"
}

variable "vpc_id" {
  type        = string
  description = "ID of the VPC where the skeleton will be deployed"
}

variable "platform_cloudwatch_alert_emails" {
  description = "List of email address will received the email from SNS when metric alarm match condition"
  type        = list(string)
  default     = []
}


# kms CMK's ARNs

variable "ssm_cmk_arn" {
  type        = string
  description = "The ARN for the SSM CMK's encryption key"
}

variable "secretsmanager_cmk_arn" {
  type        = string
  description = "The ARN for the Secrets Manager CMK's encryption key"
}

variable "sns_cmk_arn" {
  type        = string
  description = "The ARN for the SNS CMK's encryption key"
}

variable "cloudwatch_cmk_arn" {
  type        = string
  description = "The ARN for the Cloudwatch CMK's encryption key"
}

variable "sns_metric_alert_topic_arn" {
  type        = string
  description = "ARN of SNS topic dedicated for metric alerts"
}