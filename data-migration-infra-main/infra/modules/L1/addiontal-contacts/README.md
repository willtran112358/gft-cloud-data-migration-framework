## Additional-contacts
This module allows you to create 3 additional contacts (one for Security, Operations and Billing) in the AWS account. It’s mandatory to create these contacts in order to accomplish the best practises of Security Hub.

### Resources:
- aws_account_alternate_contact
This resource is the responsable to create a contact, in this case we use a for_each to create the 3 contacts necessary.
### Variables:
- additional_contacts: list(map(string))

This variable consist of a list of maps, each map is a contact with their proper values.
Each map should be key/value:
o	alternate_contact_type = {“BILLING/OPERATIONS/SECURITY”} --> String
o	name = {Name of the person} --> String
o	title = {workstation} --> String
o	email_address = {email} --> String
o	phone_number = {Number of the contact} --> String