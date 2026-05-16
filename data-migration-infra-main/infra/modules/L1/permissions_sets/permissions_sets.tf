data "aws_ssoadmin_instances" "instance" {}

resource "aws_ssoadmin_permission_set" "permission_set" {
  name         = var.name
  instance_arn = data.aws_ssoadmin_instances.instance.arn[0]
}

resource "aws_ssoadmin_permission_set_inline_policy" "example" {
  inline_policy      = var.inline_policy
  instance_arn       = data.aws_ssoadmin_instances.instance.arn[0]
  permission_set_arn = aws_ssoadmin_permission_set.permission_set.arn
}