import boto3
s3 = boto3.client('s3')
s3.download_file(
    Bucket='harita-aws-lab-2026',
    Key='uploads/from-boto3.txt',
    Filename='downloaded-from-boto3.txt'
)