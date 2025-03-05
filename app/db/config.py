from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_database_name: Optional[str] = None
    database_url: Optional[str] = None
    log_database_name: Optional[str] = None


settings = Settings()
