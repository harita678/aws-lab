import boto3
from app.config import settings

s3 = boto3.client('s3', region_name=settings.aws_region)
response = s3.list_buckets()
buckets = response['Buckets']

for b in buckets:
    print(f"Bucket Name: {b['Name']}")
