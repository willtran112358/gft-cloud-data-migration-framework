output "sns_arn" {
  description = "The sns arn"
  value       = aws_sns_topic.this.arn
}