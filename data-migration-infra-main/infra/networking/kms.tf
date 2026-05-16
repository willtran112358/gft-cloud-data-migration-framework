module "kms" {
  source = "../modules/L2/kms-networking"

  environment = var.environment
  region      = var.region
}

module "kms_lambda" {
  source = "../modules/L1/kms"
  service_name = "lambda"
}

# module "kms_cloudwatch" {
#   source = "../modules/L1/kms"
#   service_name = "cloudwatch"
# }