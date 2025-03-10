from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    maximum_logo_file_size: int = Field(default=5 * 1024 * 1024)


settings = Settings()
