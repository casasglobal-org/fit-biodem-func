import os

import boto3

FILE_URL = 'https://{bucket}.s3.eu-west-1.amazonaws.com/{filename}'
S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


def upload_to_s3(filepath, bucket=S3_BUCKET):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
# PyBites tip 172 is suboptimal because
# https://stackoverflow.com/a/60239208/8677447
    s3 = session.resource('s3')
    ret = s3.Bucket(bucket).put_object(
        Key='uploads/'+filepath.filename,
        Body=filepath.read(),
        ACL='public-read')
    return FILE_URL.format(bucket=bucket, filename=ret.key)
