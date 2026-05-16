variable "region" {
  description = "Region"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
}

variable "component" {
  type        = string
  description = "Component"
}

variable "cidr_block" {
  type        = string
  description = "VPC cidr block"
}

variable "private_subnets" {
  type        = list(string)
  description = "A list of CIDR for private subnets inside the VPC"
}

variable "protected_subnets" {
  type        = list(string)
  description = "A list of CIDR for protected subnets inside the VPC"
}

variable "public_subnets" {
  type        = list(string)
  description = "A list of CIDR for public subnets inside the VPC"
}

variable "tgw_subnets" {
  type        = list(string)
  description = "A list of CIDR for tgw subnets inside the VPC"
}

variable "domain" {
  type        = string
  description = "Domain name"
  default     = ""
}

variable "eip_allocation_ids" {
  type        = list(string)
  description = "Allocation IDs of Elastic IPs"
}

variable "kms_s3_arn" {
  type        = string
  description = "CMK for EBS"
}

variable "kms_cloudwatch_arn" {
  type        = string
  description = "CMK for EBS"
}

variable "xray_cmk_arn" {
  type        = string
  description = "X-Ray dedicated CMK key ARN"
  default     = ""
}

variable "enable_nat_gateway" {
  type        = bool
  description = "enable natgateway or not"
  default     = false
}

variable "single_nat_gateway" {
  type        = bool
  description = "single natgateway x VPC or multiple"
  default     = false
}

variable "flowlogs_bucket" {
  type        = string
  description = "flowlogs bucket in log archive account"
  default     = ""
}

# variable "kms_lambda_arn" {
#   description = "ARN of Lambda KMS key"
#   type        = string
# }
