output "eks_init" {
  value       = "aws eks update-kubeconfig --name ${var.eks_cluster_name} --region ${var.region}"
  description = "Run the following command to connect to the EKS cluster."
}

output "endpoint" {
  value = aws_eks_cluster.this.endpoint
}

output "kubeconfig-certificate-authority-data" {
  value = aws_eks_cluster.this.certificate_authority[0].data
}

output "cluster-name" {
  value = aws_eks_cluster.this.name
}