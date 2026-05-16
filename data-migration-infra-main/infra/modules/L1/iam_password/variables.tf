variable "minimum_password_length" {
  type        = number
  description = "Minimum length for the passwords"
}

variable "require_lowercase_characters" {
  type        = bool
  description = "If it's necessary a lowercase in the passwords"
}

variable "require_numbers" {
  type        = bool
  description = "If it's necessary a number in the passwords"
}

variable "require_uppercase_characters" {
  type        = bool
  description = "If it's necessary an uppercase in the passwords"
}

variable "require_symbols" {
  type        = bool
  description = "If it's necessary a symbol in the passwords"
}

variable "allow_users_to_change_password" {
  type        = bool
  description = "Allow users to change theirs passwords"
}

variable "max_password_age" {
  type        = number
  description = "The number of days that an user password is valid"
}

variable "password_reuse_prevention" {
  type        = number
  description = "The number of previous passwords that users are prevented from reusing"
}