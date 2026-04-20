import boto3
import json
from botocore.client import Config as BotoConfig
from .config import Config

def get_minio_client():
    return boto3.client(
        "s3",
        endpoint_url=f"http://{Config.MINIO_ENDPOINT}",
        aws_access_key_id=Config.MINIO_ACCESS_KEY,
        aws_secret_access_key=Config.MINIO_SECRET_KEY,
        config=BotoConfig(signature_version="s3v4"),
        region_name="us-east-1",
    )

def ensure_bucket_exists():
    client = get_minio_client()
    bucket = Config.MINIO_BUCKET
    existing = client.list_buckets()["Buckets"]
    if not any(b["Name"] == bucket for b in existing):
        client.create_bucket(Bucket=bucket)

    # публичная политика на чтение
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket}/*"
            }
        ]
    }
    client.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))

def upload_image(file_bytes: bytes, filename: str, content_type: str) -> str:
    client = get_minio_client()
    bucket = Config.MINIO_BUCKET
    client.put_object(
        Bucket=bucket,
        Key=filename,
        Body=file_bytes,
        ContentType=content_type,
    )
    return f"http://{Config.MINIO_ENDPOINT}/{bucket}/{filename}"

def delete_image(filename: str):
    client = get_minio_client()
    client.delete_object(Bucket=Config.MINIO_BUCKET, Key=filename)