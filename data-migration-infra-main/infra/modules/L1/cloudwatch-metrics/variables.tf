variable "cloudwatch-metric-name" {
  type        = string
  description = "Name of the metric"
}

variable "cloudwatch-filter-name" {
  type        = string
  description = "Name of the metric"
}

variable "cloudwatch-filter" {
  type        = string
  description = "Name of the metric"
}

variable "cloudwatch-log-group-name" {
  type        = string
  description = "Name of the metric"
}

variable "cloudwatch-metric-namespace" {
  type        = string
  description = "Name of the metric"
}

variable "metric-value" {
  type        = number
  description = "Name of the metric"
}

variable "default-metric-value" {
  type        = number
  description = "Name of the metric"
}

variable "alarm_name" {
  type        = string
  description = "Name of the alarm"
}

variable "comparison_operator" {
  type        = string
  description = "Opertator to compare"
}

variable "evaluation_periods" {
  type        = number
  description = "Periods over data is compared"
}

variable "period" {
  type        = number
  description = "Period in seconds"
}

variable "statistic" {
  type        = string
  description = "Statistic to apply to the alarm"
}

variable "threshold" {
  type        = number
  description = "Value which is compared"
}

variable "alarm_actions" {
  type        = list(string)
  description = ""
}