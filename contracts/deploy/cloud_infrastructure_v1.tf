# Cloud Infrastructure Definition v1

provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "evidence_store" {
  bucket = "vte-evidence-immutable-store"
  object_lock_configuration {
    object_lock_enabled = "Enabled"
  }
}

resource "aws_eks_cluster" "runtime" {
  name = "vte-runtime-cluster"
  # Enforce Admission Controller defined in Phase 1.40
}
