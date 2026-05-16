## Cloudwatch-metrics
In this module we create a metric filter as well as a metric alarm in order to accomplish the best practices of Security Hub. For this reason in this module we create two resources, one for the filter and the other for the alarm.

### Resources:
- aws_cloudwatch_log_metric_filter
With this resource you can create a filter for a log group.
- aws_cloudwatch_metric_alarm
In this resource you can establish an alarm that is triggered when it reach the threshold.

### Variables (aws_cloudwatch_log_metric_filter):
- cloudwatch-filter-name: String
Name of the metric filter.
- cloudwatch-filter: String
The expression of the filter.
- cloudwatch-log-group-name: String
The name of the log group where will be filtered.
- cloudwatch-metric-name: String
The name of the CloudWatch metric to which the monitored log information should be published.
- cloudwatch-metric-namespace: String
The destination namespace of the CloudWatch metric.
- metric-value: Number
The value of the condition.
- default-metric-value: Number
The default value of the condition.

### Variables (aws_cloudwatch_metric_alarm):
- alarm_name: String
The name of the alarm.
- comparison_operator: String
The arithmetic operation to use when comparing the specified Statistic and Threshold.
- evaluation_periods: Number
The number of periods over which data is compared to the specified threshold.
- period: Number
The period in seconds over which the specified statistic is applied
- statistic: String
The statistic to apply to the alarm's associated metric. Ex.(SampleCount, Average, Sum, Minimum, Maximum)
- threshold: Number
The value against which the specified statistic is compared.
- alarm_actions: list(string)
The list of actions to execute, each action an Amazon Resource Name (ARN).