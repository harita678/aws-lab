import boto3

AWS_REGION='ca-central-1'
BUCKET_NAME='harita-testpulse-raw-2026'
SQS_QUEUE_URL="https://sqs.ca-central-1.amazonaws.com/951125265513/harita-testpulse-ingestion-queue"

s3_client = boto3.client('s3', region_name=AWS_REGION)
sqs_client = boto3.client('sqs', region_name=AWS_REGION)