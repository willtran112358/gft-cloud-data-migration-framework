resource "aws_cloudwatch_log_metric_filter" "this" {
  name           = var.cloudwatch-filter-name
  pattern        = var.cloudwatch-filter
  log_group_name = var.cloudwatch-log-group-name

  metric_transformation {
    name          = var.cloudwatch-metric-name
    namespace     = var.cloudwatch-metric-namespace
    value         = var.metric-value
    default_value = var.default-metric-value
  }
}

resource "aws_cloudwatch_metric_alarm" "foobar" {
  alarm_name          = var.alarm_name
  comparison_operator = var.comparison_operator
  evaluation_periods  = var.evaluation_periods
  metric_name         = var.cloudwatch-metric-name
  namespace           = var.cloudwatch-metric-namespace
  period              = var.period
  statistic           = var.statistic
  threshold           = var.threshold
  alarm_actions       = var.alarm_actions
}