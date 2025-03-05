from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None
    github_redirect_uri: Optional[str] = None


settings = Settings()