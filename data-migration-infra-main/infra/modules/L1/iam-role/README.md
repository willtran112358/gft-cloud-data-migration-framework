## IAM-role
In this module, you can create a iam role and attach a policy with the permissions necessary.
### Rersources
- aws_iam_role
This resource creates the roles.
- aws_iam_policy
This resource can create the policy
- aws_iam_policy_attachment
The last resource attach the policy to the role

### Variables
- iam_policy_name: String
The name of the policy to be attached.
- policy: String
The policy data.
- name: String
Name of the role.
- assume_role_policy: String
Policy that grants an entity permission to assume the role.

### Outputs
- iam_role_arn: String
The iam role ARN we need to attach the policy in the "aws_iam_policy_attachment" resource.