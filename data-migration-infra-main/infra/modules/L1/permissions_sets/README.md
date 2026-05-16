## Permissions_sets
This module can create permissions sets in the management account

### Resources
For this one, we need the data "aws_ssoadmin_instances", that gets the Identity Store IDs or ARN we need for the following resources.

- aws_ssoadmin_permission_set
Creates the permission set
- aws_ssoadmin_permission_set_inline_policy
Creates and attach the permission set policy 

### Variables (aws_ssoadmin_permission_set)
- name: String
Name of the permission set.
### Variables (aws_ssoadmin_permission_set_inline_policy)
- inline_policy: String
Data policy to be attached.

### Outputs
permissions_sets_arn: String
ARN of the permissions set we created, we need it to be attached in the "aws_ssoadmin_permission_set_inline_policy" resource.