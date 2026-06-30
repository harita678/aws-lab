# ============================================================================
# sqs.tf — SQS Queue for TestPulse
# ============================================================================

resource "aws_sqs_queue" "ingestion" {
  name = var.sqs_queue_name

  tags = {
    Name        = "TestPulse Ingestion Queue"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "TestPulse"
  }
  lifecycle {
    ignore_changes = [
      max_message_size
    ]
  }
}
