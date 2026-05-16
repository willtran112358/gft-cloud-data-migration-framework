# GFT
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

# # HDBank
# terraform {
#   required_version = "~> 1.6"
#   required_providers {
#     aws = {
#       source  = "hashicorp/aws"
#       version = "~> 5.31"
#     }
#     local = {
#       version = "~> 2.4.0"
#     }
#   }
# }