variable "region" {
  type        = string
  description = "aws region"
  default     = "eu-central-1"
}

variable "environment" {
  type        = string
  description = "proyect environment, user ct for control tower configurations"
  default     = "development"
}

variable "owner" {
  type        = string
  description = "owner of the AWS resource"
  default     = "IT"
}

variable "iacgroup" {
  type        = string
  description = "owner of the AWS resource"
  default     = "UnAssign"
}

variable "aws_account" {
  type        = string
  description = "AWS account"
  default     = "<ACCOUNTID>"
}

variable "prefix" {
  type        = string
  description = "Prefix that is always at the beginning of the bucket name  and other components"
  default     = "gft-dm"
}

#VPC VARIABLES
# variable "vpc_cidr" {
#   type        = string
#   description = "vpc cidr "
#   default     = ""
# }

# variable "public_subnets" {
#   description = "A list of public subnets inside the VPC"
#   type        = list(string)
#   default     = []
# }

# variable "intra_subnets" {
#   description = "A list of public subnets inside the VPC"
#   type        = list(string)
#   default     = []
# }

# variable "private_subnets" {
#   description = "A list of private subnets inside the VPC"
#   type        = list(string)
#   default     = []
# }

# variable "private_subnets_id" {
#   description = "A list of private subnets id inside the VPC"
#   type        = list(string)
#   default     = []
# }

# EKS Variables
variable "eks_cluster_name" {
  description = "EKS Cluster name"
  type        = string
  default     = "data-migration"
}

variable "cluster_version" {
  description = "Kubernetes cluster version"
  type        = string
  default     = "1.29"
}

variable "federated_user" {
  description = "AWS Federated User"
  type        = string
}

############################################################
### GENERAL & TAGGING
############################################################
# variable "aws_profile" {
#   description = "AWS Profile used to deploy whole infrastructure"
#   type        = string
# }
variable "aws_account_id" {
  description = "AWS Account ID used to deploy whole infrastructure"
  type        = number
}
variable "aws_region" {
  description = "AWS region used to deploy whole infrastructure"
  type        = string
}
variable "aws_availability_zones" {
  description = "AWS availability zones to be used within the region"
  type        = list(string)
}
variable "env_tags" {
  type        = map(string)
  description = "Environment tags configured for all provisioned resources"
}
variable "global_tags" {
  type        = map(string)
  description = "Global tags configured for all provisioned resources"
}
variable "instance_tags" {
  type        = map(string)
  description = "Tags configured for all instance resources"
}

############################################################
### EKS Cluster
############################################################
variable "vpc_id" {
  description = "vpc_id of bastion host"
  type        = string
}

variable "subnet_ids" {
  description = "eks_subnet_ids"
  type        = list(string)
}
variable "subnets_by_zone" {
  description = "subnets_by_zone"
  type        = map(string)
}
variable "subnet_ranges" {
  description = "subnet_ranges"
  type        = list(string)
}
variable "subnets_kafka_access" {
  description = "subnets_kafka_access"
  type        = list(string)
}
variable "k8s_version" {
  description = "Kubernetes version"
  type        = string
}
variable "node_ami_name" {
  description = "Node AMI name available in the region"
  type        = string
}
variable "control_plane_access_cidrs" {
  description = "List of CIDRs that allow access to the EKS control plane"
  type        = list(string)
}
variable "eks_node_ami_type" {
  description = "Type of Amazon Machine Image (AMI) associated with the EKS Node Group. Valid values are `AL2_x86_64`, `AL2_x86_64_GPU`, `AL2_ARM_64`, `CUSTOM`, `BOTTLEROCKET_ARM_64`, `BOTTLEROCKET_x86_64`"
  type        = string
  default     = null
}
variable "eks_node_instance_types" {
  description = "List of EC2 instance type for EKS node group"
  type        = list(string)
}
variable "eks_node_disk_size" {
  description = "Disk size in GiB for nodes. Defaults to `20`. Only valid when `use_custom_launch_template` = `false`"
  type        = number
  default     = null
}
variable "desired_nodepool_size" {
  description = "Desired number of nodes"
  type        = number
}
variable "default_nodepool_max_size" {
  description = "Maximum number of nodes"
  type        = number
}
variable "default_nodepool_min_size" {
  description = "Minimum number of nodes"
  type        = number
}
variable "control_plane_subnet" {
  description = "Subnets for EKS Control Plane"
  type        = string
}
variable "node_pod_subnet" {
  description = "Subnets for Node/Pod"
  type        = string
}
variable "aws_auth_roles" {
  description = "List of role maps to add to the aws-auth configmap"
  type        = list(any)
  default     = []
}
variable "ssh_key_name" {
  description = "Name of the SSH key pair existing in AWS key pairs and used to authenticate to VM-Series or test boxes"
  type        = string
}

variable "instance_type_overides" {
  description = "Instance sizing overides for worker pool on EKS cluster"
  type        = string
}

variable "use_spot_instances" {
  description = "Enable or disable use spot instance for worker pool on EKS cluster"
  type        = bool
}
variable "ebs_addon_version" {
  description = "aws-ebs-csi-driver addon version"
  type        = string
  default     = "v1.40.1-eksbuild.1"
}

variable "efs_addon_version" {
  description = "aws-ebs-csi-driver addon version"
  type        = string
  default     = "v1.7.7-eksbuild.1"
}
variable "otel_addon_version" {
  description = "aws-ebs-csi-driver addon version"
  type        = string
  default     = "v0.43.0-eksbuild.1"
}

variable "enable_ebs_csi_driver" {
  description = "Whether to enable the EBS CSI Driver addon"
  type        = bool
  default     = true
}

variable "enable_efs_csi_driver" {
  description = "Whether to enable the EFS CSI Driver addon"
  type        = bool
  default     = true
}

variable "enable_otel_collector" {
  description = "Whether to enable the AWS Distro for OpenTelemetry (ADOT) addon"
  type        = bool
  default     = false
}
variable "enable_fluentbit_cloudwatch" {
  description = "Enable IAM role for AWS Load Balancer Controller"
  type        = bool
  default     = false
}
variable "enable_lb_controller" {
  description = "Enable IAM role for AWS Load Balancer Controller"
  type        = bool
  default     = false
}

############################################################
### Route 53
############################################################
variable "domain_name" {
  description = "Domain name which is accibles via route 53 to create subdomains under for Thought Machine Vault services access"
  type        = string
}
variable "db_record_name" {
  description = "Name of the private route53 zone record mapping to RDS."
}

############################################################
### AWS KMS
############################################################
variable "kms_alias_name" {
  description = "The display name of the alias. The name must start with the word \"alias\" followed by a forward slash (alias/)"
  type        = string
}

############################################################
### SecretManager
############################################################

variable "secret_managers" {
  type = any
}

############################################################
### Aurora for PostgreSQL
############################################################
variable "use_aurora" {
  type        = bool
  description = "Use AWS Aurora instead of regular RDS instances. Defaults to false."
  default     = false
}

variable "db_name" {
  description = "Database Name"
  type        = string
}

variable "db_family" {
  description = "AWS RDS Database family name"
  type        = string
}
variable "db_version" {
  description = "Database version to be used in RDS"
  type        = string
}
variable "db_username" {
  description = "Username to be used in RDS"
  type        = string
}
variable "db_secret_manager" {
  description = "Database secret manager"
  type        = string
}
variable "db_storage_type" {
  description = "Storage type to be used in RDS"
  type        = string
}
variable "db_instance_class" {
  description = "Database instance class to be used"
  type        = string
}
variable "db_allocated_storage" {
  description = "Allocated storage in GiB"
  type        = number
}
variable "db_max_allocated_storage" {
  description = "Upper limit of storage when scaled in GiB"
  type        = number
}
# variable "db_subnet_group" {
#   description = "Subnet name to used for DB Subnet Group"
#   type        = string
# }
variable "db_multi_az" {
  description = "RDS with Multi Availabe Zone"
  type        = bool
  default     = true
}
variable "db_deletion_protection" {
  description = "RDS Deletion Protection"
  type        = bool
  default     = true
}
variable "db_performance_insights_enabled" {
  description = "RDS Performance Insight"
  type        = bool
  default     = false
}
variable "db_backup_window" {
  description = "Time frame in UTC to perform backups (hh:mm-hh:mm)"
  type        = string
}
variable "db_backup_retention_period" {
  description = "RDS backup retention period (in days)"
  type        = number
}
variable "db_maintenance_window" {
  description = "Time frame to perform maintenance (ddd:hh:mm-ddd:hh:mm)"
  type        = string
}
variable "db_parameter_group" {
  description = "Time frame to perform maintenance (ddd:hh:mm-ddd:hh:mm)"
  type = list(object({
    name         = string
    value        = string
    apply_method = string
  }))
}

variable "project" {
  description = "project"
  type        = string
}

# variable "environment" {
#   description = "environment"
#   type        = string
# }

variable "rds_cidr_range" {
  description = "List of CIDR blocks that are allowed to access the MSK cluster"
  type        = list(string)
  default     = []
}

variable "db_subnet_group" {
  description = "List of db_subnet_group"
  type        = list(string)
  default     = []
}

############################################################
### AWS MSK
############################################################
variable "kafka_version" {
  description = "Kafka version for the MSK cluster"
  type        = string
}

variable "number_of_broker_nodes" {
  description = "Number of broker nodes in the cluster"
  type        = number
}

variable "broker_node_group_info" {
  description = "Configuration for the broker node group"
  type = object({
    instance_type   = string
    ebs_volume_size = number
    subnet          = string
  })
}

variable "msk_primary_key" {
  description = "MSK primary key is unique to be used for identify secret manager is belong to"
  type        = string
}

variable "add_msk_secret" {
  type        = bool
  default     = false
  description = "enable/disable add secret to msk which created by vault core"
}

variable "secret_arn_list" {
  description = "secret arn list"
  type        = list(string)
}

# variable "msk_scram_secret_association" {
#   description = "msk_scram_secret_association"
#   type = list(string)
# }

variable "msk_allowed_cidrs" {
  description = "List of CIDR blocks that are allowed to access the MSK cluster"
  type        = list(string)
  default     = []
}

variable "msk_subnet_ids" {
  description = "List of CIDR blocks that are allowed to access the MSK cluster"
  type        = list(string)
  default     = []
}
variable "vpcs" {
  description = <<-EOF
  A map defining VPCs with security groups and subnets.

  Following properties are available:
  - `name`: VPC name
  - `cidr`: CIDR for VPC
  - `subnets`: map of subnets with properties:
     - `az`: availability zone
     - `set`: internal identifier referenced by main.tf
  - `security_groups`: map of security groups
  - `routes`: map of routes with properties:
     - `vpc_subnet` - built from key of VPCs concatenate with `-` and key of subnet in format: `VPCKEY-SUBNETKEY`
     - `next_hop_key` - must match keys use to create TGW attachment, IGW, GWLB endpoint or other resources
     - `next_hop_type` - internet_gateway, nat_gateway, transit_gateway_attachment or gwlbe_endpoint

  Example:
  ```
  vpcs = {
    example_vpc = {
      name = "example-spoke-vpc"
      cidr = "10.104.0.0/16"
      nacls = {
        trusted_path_monitoring = {
          name               = "trusted-path-monitoring"
          rules = {
            allow_inbound = {
              rule_number = 300
              egress      = false
              protocol    = "-1"
              rule_action = "allow"
              cidr_block  = "0.0.0.0/0"
              from_port   = null
              to_port     = null
            }
          }
        }
      }
      security_groups = {
        example_vm = {
          name = "example_vm"
          rules = {
            all_outbound = {
              description = "Permit All traffic outbound"
              type        = "egress", from_port = "0", to_port = "0", protocol = "-1"
              cidr_blocks = ["0.0.0.0/0"]
            }
          }
        }
      }
      subnets = {
        "10.104.0.0/24"   = { az = "ap-southeast-1a", set = "vm", nacl = null }
        "10.104.128.0/24" = { az = "ap-southeast-1b", set = "vm", nacl = null }
      }
      routes = {
        vm_default = {
          vpc_subnet    = "app1_vpc-app1_vm"
          to_cidr       = "0.0.0.0/0"
          next_hop_key  = "app1"
          next_hop_type = "transit_gateway_attachment"
        }
      }
    }
  }
  ```
  EOF
  default     = {}
  type = map(object({
    name      = string
    cidr      = string
    sub_cidrs = list(string)
    security_groups = map(object({
      name = string
      rules = map(object({
        description = string
        type        = string,
        from_port   = string
        to_port     = string,
        protocol    = string
        cidr_blocks = list(string)
      }))
    }))
    subnets = map(object({
      az   = string
      set  = string
      nacl = string
    }))
    routes = map(object({
      vpc_subnet    = string
      to_cidr       = string
      next_hop_key  = string
      next_hop_type = string
    }))
  }))
}