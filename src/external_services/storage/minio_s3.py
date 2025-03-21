from contextlib import asynccontextmanager
from typing import Annotated, BinaryIO

import aiobotocore.session
from botocore.exceptions import ClientError
from fastapi import Depends

from src.config.project_settings import Settings, get_settings
from src.consts import StorageType
from src.external_services.storage.base import FileStorage


class S3StorageClient(FileStorage):
    def __init__(self, access_key: str, secret_key: str, url: str, bucket_name: str):
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url

    @asynccontextmanager
    async def get_client(self):
        session = aiobotocore.session.get_session()
        async with session.create_client(
            "s3",
            endpoint_url=self.url,
            aws_secret_access_key=self.secret_key,
            aws_access_key_id=self.access_key,
        ) as client:
            yield client

    async def upload_file(self, payload: BinaryIO, path: str) -> None:
        async with self.get_client() as client:
            return await client.put_object(
                Bucket=self.bucket_name,
                Key=path,
                Body=payload,
            )

    async def get_file(self, path):
        async with self.get_client() as client:
            try:
                response = await client.get_object(Bucket=self.bucket_name, Key=path)
                return await response["Body"].read()
            except ClientError as e:
                if e.response["Error"]["Code"] == "NoSuchKey":
                    return None

    async def delete_file(self, path):
        async with self.get_client() as client:
            await client.delete_object(
                Bucket=self.bucket_name,
                Key=path,
            )

    async def get_file_link(self, path):
        async with self.get_client() as client:
            return await client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self.bucket_name, "Key": path},
            )


def get_file_storage(
    settings: Annotated[Settings, Depends(get_settings)],
) -> FileStorage:
    if settings.storage_type == StorageType.S3:
        return S3StorageClient(
            access_key=settings.s3_access_key,
            secret_key=settings.s3_secret_key,
            url=settings.s3_url,
            bucket_name=settings.s3_bucket_name,
        )
