output "iam_role_arn" {
  description = "The iam role arn"
  value       = aws_iam_role.this.arn
}