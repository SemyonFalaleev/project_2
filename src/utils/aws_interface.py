import json
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from fastapi import UploadFile
from decouple import config
from uuid import uuid4


class AWSClient:
    def __init__(
        self,
        url: str,
        access_key_id: str,
        secret_access_key: str,
        bucket_name: str,
        public: bool = False,
    ):
        self.bucket_name = bucket_name
        self.url = url
        self.public = public
        self.s3 = boto3.client(
            "s3",
            endpoint_url=url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                self.s3.create_bucket(Bucket=self.bucket_name)
                self.s3.put_bucket_policy(
                    Bucket=self.bucket_name, Policy=self._public_bucket_policy()
                )

    def _public_bucket_policy(self) -> str:
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject"
                    if self.public
                    else "PrivateAccessPolicy",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{self.bucket_name}/*",
                }
            ],
        }
        return json.dumps(policy)

    def upload_file_from_stream(self, file: UploadFile):
        key = uuid4()
        self.s3.upload_fileobj(Fileobj=file.file, Bucket=self.bucket_name, Key=str(key))
        return f"{self.bucket_name}/{key}"

    def delete_file_from_bucket(self, file_name: str):
        self.s3.delete_object(Bucket=self.bucket_name, Key=file_name.split("/")[1])


client_s3 = AWSClient(
    config("AWS_URL"),
    config("AWS_ACCESS_KEY_ID"),
    config("AWS_SECRET_ACCESS_KEY"),
    bucket_name="uploads",
    public=True,
)
