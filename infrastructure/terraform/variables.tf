variable "aws_region" {
  description = "AWS Region"
  default     = "us-east-1"
}

output "cluster_endpoint" {
  description = "EKS Control Plane Endpoint"
  value       = module.eks.cluster_endpoint
}

output "db_endpoint" {
  description = "RDS Endpoint"
  value       = module.db.db_instance_endpoint
}
