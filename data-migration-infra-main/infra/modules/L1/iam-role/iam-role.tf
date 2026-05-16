#create resource aws_iam_policy if var.iam_policy_name is not null
resource "aws_iam_policy" "iam_policy" {
  count = var.iam_policy_name != "" ? 1 : 0

  name        = var.iam_policy_name
  description = "IAM Policy"
  policy      = var.policy
}

resource "aws_iam_role" "this" {
  name = var.name

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = var.assume_role_policy
  #managed_policy_arns = join(",",  var.managed_policy_arns, (var.iam_policy_name != "" ? aws_iam_policy.iam_policy[0].arn : "arn:aws:iam::aws:policy/AWSDenyAll"))

}



# resource "aws_iam_policy_attachment" "iam_policy_attachment" {
#   for_each = var.iam_policy_name != "" ? toset([1]) : toset([])

#   name       = "Policy Attachement"
#   policy_arn = aws_iam_policy.iam_policy.arn
#   roles      = [aws_iam_role.this.name]
# }

#create resource attachment if var.iam_policy_name is not null
# resource "aws_iam_policy_attachment" "iam_policy_attachment" {
#   count = var.iam_policy_name != "" ? 1 : 0

#   name       = "Policy-Attachement"
#   policy_arn = aws_iam_policy.iam_policy[0].arn
#   roles      = [aws_iam_role.this.name]
# }

#attach policy if var.managed_policy_arns is not null to aws_iam_role

resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment" {
  count = length(var.managed_policy_arns)

  role       = aws_iam_role.this.name
  policy_arn = var.managed_policy_arns[count.index]
}

#attach managed policy if var.iam_policy_name is not null to aws_iam_role

resource "aws_iam_role_policy_attachment" "ec2_policy_attachment" {
  count = var.iam_policy_name != "" ? 1 : 0

  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.iam_policy[count.index].arn
}

resource "aws_iam_instance_profile" "this" {
  name = aws_iam_role.this.name
  role = aws_iam_role.this.name
}