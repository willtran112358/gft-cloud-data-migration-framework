variable "dynamodb_name" {
  type        = string
  description = "Name of the dynamodb table"
}

variable "billing_mode" {
  type        = string
  description = "Billing mode"
}

variable "read_capacity" {
  type        = number
  description = "Number of read units"
}

variable "write_capacity" {
  type        = number
  description = "Number of write units"
}

variable "hash_key" {
  type        = string
  description = "Hash (partition) key"
}

variable "range_key" {
  type        = string
  description = "Range  (sort) key"
}