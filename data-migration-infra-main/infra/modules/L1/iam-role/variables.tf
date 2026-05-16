variable "iam_policy_name" {
  type        = string
  description = "Name of the role policy"
  default     = ""
}

variable "policy" {
  type        = string
  description = "Policy of the role"
  default     = ""
}

variable "name" {
  type        = string
  description = "Name of the role"
  default     = ""
}

variable "assume_role_policy" {
  type        = string
  description = ""
}

variable "managed_policy_arns" {
  type        = list(string)
  description = "list of managed policy to attach in a role"
  default     = []
}