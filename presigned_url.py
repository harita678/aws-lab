import boto3

s3 = boto3.client('s3')

url = s3.generate_presigned_url('get_object', Params={
    'Bucket': 'harita-aws-lab-2026',
    'Key': 'uploads/from-boto3.txt'
},
ExpiresIn=60)

print(f"url: {url}")