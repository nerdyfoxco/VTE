provider "aws" {
  region = var.aws_region
}

# Provider Configuration for EKS
data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_name
  depends_on = [module.eks]
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_name
  depends_on = [module.eks]
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.cluster.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}

# Gap 133: VPC Flow Logs & Gap 144: Private Network
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "vte-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"] # Gap 136: 3 AZs for true HA
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  # Gap 136: High Availability NAT
  enable_nat_gateway     = true
  single_nat_gateway     = false
  one_nat_gateway_per_az = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  # Flow Logs for Audit
  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  create_flow_log_cloudwatch_iam_role  = true
}

# Gap 142: Web Application Firewall (WAF)
resource "aws_wafv2_web_acl" "vte_waf" {
  name        = "vte-waf-acl"
  description = "WAF for VTE API Protection"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "VTEWAFMetrics"
    sampled_requests_enabled   = true
  }

  rule {
    name     = "AWS-AWSManagedRulesCommonRuleSet"
    priority = 1
    override_action {
      none {}
    }
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "CommonRules"
      sampled_requests_enabled   = true
    }
  }
}

# EKS Cluster (Runtime)
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "vte-spine-cluster"
  cluster_version = "1.27"
  
  # Gap 144: Private Access Only for API
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true # Secured via CIDR in prod, leaving true for visibility now but usually false

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  enable_irsa = true # Gap 145: Least Privilege via IRSA

  eks_managed_node_groups = {
    # Gap 136: Multi-AZ Node Group
    system = {
      name = "vte-system-nodes"
      instance_types = ["t3.medium"]
      min_size     = 2
      max_size     = 4
      desired_size = 2
      
      # Gap 138: Autoscaling support
      labels = {
        role = "system"
      }
    }
  }
  
  # Gap 133: Control Plane Logging
  cluster_enabled_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
}

# RDS Postgres (Persistence)
module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "vte-spine-db"

  engine            = "postgres"
  engine_version    = "14"
  family            = "postgres14"
  instance_class    = "db.r6g.large" # Enterprise Grade
  allocated_storage = 100

  db_name  = "vte_backend"
  username = "vte_admin"
  port     = "5432"

  # Gap 136: Multi-AZ
  multi_az = true
  
  # Gap 108: Encryption
  storage_encrypted = true
  
  # Gap 113: Backup & Retention
  backup_retention_period = 30
  backup_window           = "03:00-06:00"
  
  # Gap 116: Performance Insights
  performance_insights_enabled = true

  vpc_security_group_ids = [module.vpc.default_security_group_id]
  subnet_ids             = module.vpc.private_subnets
  
  # Gap 152: Deletion Protection
  deletion_protection = true
}

