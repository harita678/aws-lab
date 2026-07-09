# ============================================================================
# cloudwatch.tf — Observability: log retention, metrics, alarms
# ============================================================================

resource "aws_cloudwatch_log_group" "lambda_processor" {
  name              = "/aws/lambda/harita-testpulse-processor"
  retention_in_days = 14

  tags = {
    Name        = "TestPulse Lambda Logs"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "TestPulse"
  }
}
# --- Saved Logs Insights queries (version-controlled) ---

resource "aws_cloudwatch_query_definition" "lambda_performance" {
  name = "TestPulse/Lambda-Performance"

  log_group_names = [
    aws_cloudwatch_log_group.lambda_processor.name
  ]

  query_string = <<-QUERY
    filter @type = "REPORT"
    | stats avg(@duration) as avg_ms, max(@duration) as max_ms, pct(@duration, 95) as p95_ms
  QUERY
}

resource "aws_cloudwatch_query_definition" "lambda_invocations" {
  name = "TestPulse/Run-Count"

  log_group_names = [
    aws_cloudwatch_log_group.lambda_processor.name
  ]

  query_string = <<-QUERY
    fields @message
    | filter @message like /Ingestion ID/
    | parse @message "Ingestion ID: *" as ingestion_id
    | stats count(*) as total_runs
  QUERY
}