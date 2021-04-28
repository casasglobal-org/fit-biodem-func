import os

import boto3

FILE_URL = 'https://{bucket}.s3.eu-west-1.amazonaws.com/{filename}'
S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')


def upload_to_s3(filename, body, folder="uploads",
                 bucket=S3_BUCKET, region_name=AWS_REGION_NAME):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=region_name
    )
    print(region_name)
    # PyBites tip 172 is suboptimal because
    # https://stackoverflow.com/a/60239208/8677447
    s3 = session.resource('s3')
    ret = s3.Bucket(bucket).put_object(
        Key=f"{folder}/{os.path.basename(filename)}",
        Body=body,
        ACL='public-read') # ContentType='image/png'

    return FILE_URL.format(bucket=bucket, filename=ret.key)


def retrieve_from_s3(file_name, bucket_name=S3_BUCKET):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    obj = bucket.Object(key=file_name)
    response = obj.get()
    data = response['Body'].read().decode('utf-8')
    return data
