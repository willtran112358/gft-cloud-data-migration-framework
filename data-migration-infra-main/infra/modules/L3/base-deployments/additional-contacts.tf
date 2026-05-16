resource "aws_account_alternate_contact" "operations" {
  count = length(var.additional_contacts)

  alternate_contact_type = var.additional_contacts[count.index]["alternate_contact_type"]

  name          = var.additional_contacts[count.index]["name"]
  title         = var.additional_contacts[count.index]["title"]
  email_address = var.additional_contacts[count.index]["email_address"]
  phone_number  = var.additional_contacts[count.index]["phone_number"]
}