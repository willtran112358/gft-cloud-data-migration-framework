# ################################################################################
# # VPC Module
# ################################################################################
# locals {
#   network_acls = {
#     default_inbound = [

#     ]
#     default_outbound = [
#       {
#         rule_number = 1
#         protocol    = "tcp"
#         rule_action = "allow"
#         cidr_block  = "0.0.0.0/0"
#         from_port   = 1
#         to_port     = 65535
#       },
#     ]
#     private_inbound = [
#       {
#         rule_number = 100
#         rule_action = "allow"
#         from_port   = 1
#         to_port     = 65535
#         protocol    = "tcp"
#         cidr_block  = "0.0.0.0/0"
#       }
#     ]
#     private_outbound = [
#       {
#         rule_number = 100
#         rule_action = "allow"
#         from_port   = 1
#         to_port     = 65535
#         protocol    = "-1"
#         cidr_block  = "0.0.0.0/0"
#       }
#     ]

#   }
# }

# # CloudWatch Log Group and IAM role created automatically
# module "vpc_with_flow_logs_cloudwatch_logs_default" {
#   source = "../modules/L2/vpc"

#   name               = "${var.component}-vpc"
#   cidr               = var.vpc_cidr
#   azs                = local.azs
#   enable_nat_gateway = true
#   single_nat_gateway = false

#   public_subnets  = var.public_subnets
#   private_subnets = var.private_subnets
#   intra_subnets   = var.intra_subnets

#   map_public_ip_on_launch = true
#   enable_dns_hostnames    = true
#   enable_dns_support      = true

#   public_subnet_tags = {
#     "kubernetes.io/role/elb" = 1
#   }

#   private_subnet_tags = {
#     "kubernetes.io/role/internal-elb" = 1
#   }

#   # Cloudwatch log group and IAM role will be created
#   enable_flow_log                      = true
#   create_flow_log_cloudwatch_log_group = true
#   create_flow_log_cloudwatch_iam_role  = true

#   flow_log_max_aggregation_interval         = 60
#   flow_log_cloudwatch_log_group_name_prefix = "/aws/vpc-flow-logs/"
#   flow_log_cloudwatch_log_group_name_suffix = var.component
#   flow_log_cloudwatch_log_group_kms_key_id  = module.kms.kms_cloudwatch_arn

#   private_dedicated_network_acl = true
#   private_inbound_acl_rules     = concat(local.network_acls["private_inbound"])
#   private_outbound_acl_rules    = concat(local.network_acls["private_outbound"])

# }

################################################################################
# Supporting Resources
################################################################################

resource "aws_iam_role" "vpc_flow_log_cloudwatch" {
  name_prefix        = "vpc-flow-log-role-"
  assume_role_policy = data.aws_iam_policy_document.flow_log_cloudwatch_assume_role.json
}

data "aws_iam_policy_document" "flow_log_cloudwatch_assume_role" {
  statement {
    principals {
      type        = "Service"
      identifiers = ["vpc-flow-logs.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role_policy_attachment" "vpc_flow_log_cloudwatch" {
  role       = aws_iam_role.vpc_flow_log_cloudwatch.name
  policy_arn = aws_iam_policy.vpc_flow_log_cloudwatch.arn
}

resource "aws_iam_policy" "vpc_flow_log_cloudwatch" {
  name_prefix = "vpc-flow-log-cloudwatch-"
  policy      = data.aws_iam_policy_document.vpc_flow_log_cloudwatch.json
}

data "aws_iam_policy_document" "vpc_flow_log_cloudwatch" {
  statement {
    sid = "AWSVPCFlowLogsPushToCloudWatch"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
    ]

    resources = ["*"]
  }
}

# #additional flow log to s3
# resource "aws_flow_log" "s3_flow_logs" {
#   log_destination      = module.s3_flowlogs.bucket_arn
#   log_destination_type = "s3"
#   traffic_type         = "ALL"
#   vpc_id               = "vpc-0962cb9f6bcc7a99a"
#   destination_options {
#     file_format                = "parquet"
#     hive_compatible_partitions = true
#   }
# }
