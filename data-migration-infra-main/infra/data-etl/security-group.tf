module "lambdas_security_group" {
  source = "../modules/L2/security-group"

  use_name_prefix = false
  # name            = "${var.prefix}-lambdas-sg"
  # HDBank edit
  name            = "${var.prefix}-lambdas-sg-edit"
  description     = "Security group for Lambda Function"
  vpc_id          = local.vpc_id

  ingress_rules       = ["all-all"]
  ingress_cidr_blocks = ["0.0.0.0/0"]

  egress_rules       = ["all-all"]
  egress_cidr_blocks = ["0.0.0.0/0"]


}
