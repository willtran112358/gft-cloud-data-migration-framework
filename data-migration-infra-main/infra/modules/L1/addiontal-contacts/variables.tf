variable "additional_contacts" {
  type        = list(map(string))
  description = "List of map where would be the contacts for BILLING, OPERATIONS, SECURITY"
}