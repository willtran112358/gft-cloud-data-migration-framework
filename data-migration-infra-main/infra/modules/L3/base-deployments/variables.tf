variable "minimum_password_length" {
  type        = number
  description = "value"
  default     = 14
}

variable "max_password_age" {
  type        = number
  description = "maximun time in day for password expiration "
  default     = 90
}

variable "require_lowercase_characters" {
  type        = bool
  description = "value"
  default     = true
}

variable "require_numbers" {
  type        = bool
  description = "value"
  default     = true
}

variable "require_uppercase_characters" {
  type        = bool
  description = "value"
  default     = true
}

variable "require_symbols" {
  type        = bool
  description = "value"
  default     = true
}

variable "allow_users_to_change_password" {
  type        = bool
  description = "value"
}

variable "additional_contacts" {
  type        = list(map(string))
  description = "List of map where would be the contacts for BILLING, OPERATIONS, SECURITY"
}

variable "account_name" {
  type        = string
  description = "aws account name"
}

variable "password_reuse_prevention" {
  type        = number
  description = "The number of previous passwords that users are prevented from reusing"
  default     = 24
}