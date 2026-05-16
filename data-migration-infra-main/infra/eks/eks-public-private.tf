resource "aws_iam_role" "eks" {
  name = "${var.prefix}-eks-cluster-${var.eks_cluster_name}"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "eks_amazon_eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks.name
}

resource "aws_eks_cluster" "this" {
  name     = "${var.cluster_prefix}-${var.eks_cluster_name}"
  version  = var.cluster_version
  role_arn = aws_iam_role.eks.arn

  vpc_config {
    subnet_ids = concat(
      local.private_subnets_ids,
      local.public_subnets_ids
    )
  }

  access_config {
    authentication_mode                         = "API_AND_CONFIG_MAP"
    bootstrap_cluster_creator_admin_permissions = true
  }

  depends_on = [aws_iam_role_policy_attachment.eks_amazon_eks_cluster_policy]
}
