## SNS
With this module we can create a SNS following the best practices.

### Resources
- aws_sns_topic
This resource creates the Topic.
- aws_sns_topic_subscription
This resource creates the subscription to the topic.

### Variables (aws_sns_topic)
- name: String
The name of the topic
- kms_master_key_id: String
The ID of an AWS-managed customer master key
- lambda_success_feedback_role_arn: String
(Optional) Lambda ARN function when there is a success
- lambda_success_feedback_sample_rate: String
(Optional) Lambda ARN function percentage of success.
- lambda_failure_feedback_role_arn: String
(Optional) Lambda ARN function when there is a failure.
- policy_topic: String
A data policy that contains the specifications of the resource. (If is empty it will use the default policy)

### Variables (aws_sns_topic_subscription)
- endpoint: list(string)
If we want to add multiples subscription we can create a list with all the emails to attach, this resource does a for_each which is every email in the list, each email will be the endpoint.
- protocol: String
Protocol to use. Valid values are: sqs, sms, lambda, firehose, application, email, email-json, http and https