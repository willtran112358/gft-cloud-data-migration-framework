

resource "aws_security_group_rule" "allow_web" {
  type              = "ingress"
  from_port         = 80
  to_port           = 8080
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_eks_cluster.this.vpc_config[0].cluster_security_group_id
}

resource "aws_security_group_rule" "allow_web_node_port" {
  type              = "ingress"
  from_port         = 30000
  to_port           = 40000
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_eks_cluster.this.vpc_config[0].cluster_security_group_id
}

# resource "aws_security_group_rule" "allow_web_node_port" {
#   type              = "ingress"
#   from_port         = 9443
#   to_port           = 9443
#   protocol          = "tcp"
#   cidr_blocks       = ["0.0.0.0/0"]
#   security_group_id = aws_eks_cluster.this.vpc_config[0].cluster_security_group_id
# }

module "lambdas_security_group" {
  source = "../modules/L2/security-group"

  use_name_prefix = false
  name            = "${var.prefix}-lambdas-sg"
  description     = "Security group for Lambda Function"
  vpc_id          = local.vpc_id

  ingress_rules       = ["all-all"]
  ingress_cidr_blocks = ["0.0.0.0/0"]

  egress_rules       = ["all-all"]
  egress_cidr_blocks = ["0.0.0.0/0"]


}
