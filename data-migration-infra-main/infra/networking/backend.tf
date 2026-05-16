# HDBank Centralized Terraform State Backend
terraform {
  backend "s3" {
    bucket         = "s3-bucket-apse1-uat-cicd-terraform-backend" # S3 bucket used for storing terraform state
    key            = "uat/digital-core-uat/terraform-data-migration-infra-networking.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "data-migration-uat-terraform-states-lock-699955796816-ap-southeast-1" # AWS account profile
    encrypt        = "true"
  }
}