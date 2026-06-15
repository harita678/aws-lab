import boto3

s3= boto3.client('s3')


response = s3.list_objects_v2(Bucket='harita-aws-lab-2026')
objects = response['Contents']

print(f"no of objects: {len(objects)}")

for object in objects:
    print(f"file name: {object['Key']}, file size: {object['Size']}, Updated: {object['LastModified']} ")