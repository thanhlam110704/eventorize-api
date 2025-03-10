from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str = Field(default='apac')
    public_url: str
    event_bucket_name: str = Field(default='event')
    avatar_folder_name: str = Field(default='user-avatars')


settings = Settings()
