# ============================================================================
# variables.tf — Input variables for TestPulse infrastructure
# ============================================================================

variable "region" {
  description = "Region name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "sqs_queue_name" {
  description = "Name of the SQS queue for integration events"
  type        = string
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket name"
  type        = string
}

variable "lambda_role_name" {
  description = "Name of the IAM Role that Lambda function will assume"
  type        = string
}

variable "ec2_role_name" {
  description = "Name of IAM Role that EC2 will assume"
  type        = string
}