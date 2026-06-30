# ============================================================================
# main.tf — Terraform foundation for TestPulse
# ============================================================================

terraform {
    required_version = ">= 1.0"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version ="~>5.0"
        }
    }
}

# Provider config

provider "aws" {
    region = var.region

}