from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    vat: float = Field(default=0.1)


settings = Settings()
