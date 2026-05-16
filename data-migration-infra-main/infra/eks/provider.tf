provider "aws" {
  allowed_account_ids = [var.aws_account_id]
  region              = var.aws_region
  # assume_role {
  #   role_arn = "arn:aws:iam::699955796816:role/iam-role-terraform-deployment"
  # }
  default_tags {
    tags = var.global_tags
  }
}
#provider "kubernetes" {
#  config_path = "~/.kube/config" # Ruta a tu archivo kubeconfig 
#}
