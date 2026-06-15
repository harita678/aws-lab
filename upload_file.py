import boto3
s3 = boto3.client('s3')

s3.upload_file(
    Filename='test-upload.txt',
    Bucket='harita-aws-lab-2026',
    Key='uploads/from-boto3.txt'
)

print("upload complete")
