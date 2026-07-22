import boto3
import os

AWS_REGION=os.environ["AWS_REGION"]
BUCKET_NAME=os.environ["S3_BUCKET_NAME"]
SQS_QUEUE_URL=os.environ["SQS_QUEUE_URL"]

s3_client = boto3.client('s3', region_name=AWS_REGION)
sqs_client = boto3.client('sqs', region_name=AWS_REGION)