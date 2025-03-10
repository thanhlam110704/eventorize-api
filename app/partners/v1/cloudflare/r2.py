import io

import boto3

from .config import settings
from .exceptions import R2ErrorCode


class R2Services:
    def __init__(self, public_url: str, endpoint_url: str, aws_access_key_id: str, aws_secret_access_key: str, region_name: str, bucket_name: str, folder_name: str) -> None:
        self.public_url = public_url
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.bucket_name = bucket_name
        self.folder_name = folder_name

        self.s3 = boto3.client(
            service_name="s3", endpoint_url=self.endpoint_url, aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name=self.region_name
        )

    async def upload_file(self, filename: str, file_path: str = None, file_content: bytes = None) -> str:
        if not file_path and not file_content:
            raise ValueError("Either file_path or file_content must be provided")
        if file_path and file_content:
            raise ValueError("Only one of file_path or file_content must be provided")
        if file_path:
            with open(file_path, "rb") as file:
                file_content = file.read()
        file_key_name = f"{self.folder_name}/{filename}"
        try:
            self.s3.upload_fileobj(io.BytesIO(file_content), self.bucket_name, file_key_name)
            public_url = f"{self.public_url}/{file_key_name}"
            return public_url
        except Exception:
            raise R2ErrorCode.UploadFailed()


r2_services = R2Services(
    public_url=settings.public_url,
    endpoint_url=settings.endpoint_url,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.region_name,
    bucket_name=settings.event_bucket_name,
    folder_name=settings.avatar_folder_name,
)
