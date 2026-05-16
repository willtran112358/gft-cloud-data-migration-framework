## IAM_password
This module allows you to change the policy of the password, being more restrictive or less
### Resources
- aws_iam_account_password_policy
This resource updates de the policy of the password.
### Variables
- minimum_password_length: Number
The minimum password length is allowed to create.
- require_lowercase_characters: Boolean
If is obligatory to include a lowercase in the password.
- require_numbers: Boolean
If is obligatory to include a number in the password.
- require_uppercase_characters: Boolean
If is obligatory to include a uppercase in the password.
- require_symbols: Boolean
If is obligatory to include a symbol in the password.
- allow_users_to_change_password: Boolean
If a user can change the password.
