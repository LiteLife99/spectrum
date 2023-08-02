import boto3
from typing import Dict
from utils.configUtil import config

s3_client = boto3.client(
    "s3",
    aws_access_key_id=config["aws_access_key_id"],
    aws_secret_access_key=config["aws_secret_access_key"],
    region_name=config["region_name"],
)

def get_s3_object(s3bucket: str, s3key: str) -> Dict:
    s3_object = s3_client.get_object(Bucket=s3bucket, Key=s3key)
    return s3_object

def push_to_s3(local_file_path : str, bucket_name : str, object_key: str):
    uploaded = s3_client.upload_file(local_file_path, bucket_name, object_key)
    return uploaded

def fetch_presigned_url(s3bucket: str, s3key: str, expiry: int = 3600):
    s3_presigned_url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': s3bucket,
            'Key': s3key
        },
        ExpiresIn=expiry
    )
    return s3_presigned_url