from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    client_id_google: Optional[str] = None
    client_secret_google: Optional[str] = None
    redirect_uri_google: Optional[str] = None


settings = Settings()