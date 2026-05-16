output "aws_secretsmanager_secret" {
  value = aws_secretsmanager_secret.this
}

output "aws_secretsmanager_secret_version" {
  value = var.create_password ? aws_secretsmanager_secret_version.data_with_password : aws_secretsmanager_secret_version.data
}

output "password" {
  value = var.create_password ? random_string.random_password[0].result : ""
}

output "belong" {
  value = var.belong
}