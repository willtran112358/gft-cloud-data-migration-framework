module "vpc" {
  source = "../../L2/default-vpc"

  region             = var.region
  environment        = var.environment
  component          = var.component
  domain             = var.domain
  enable_nat_gateway = var.enable_nat_gateway
  single_nat_gateway = var.single_nat_gateway

  cidr_block         = var.cidr_block
  public_subnets     = var.public_subnets
  private_subnets    = var.private_subnets
  protected_subnets  = var.protected_subnets
  tgw_subnets        = var.tgw_subnets
  eip_allocation_ids = var.eip_allocation_ids
  kms_s3             = var.kms_s3_arn
  flowlogs_bucket    = var.flowlogs_bucket
  kms_cloudwatch_arn = var.kms_cloudwatch_arn

}
