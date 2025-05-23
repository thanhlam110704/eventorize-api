from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    resend_api_key: Optional[str] = None
    host_email: str = Field(default="no-reply@eventorize-api-thanhlam.site")
    sender_name: str = Field(default="Eventorize")
    verification_link: str = Field(default="https://eventorize-api-thanhlam.siteverify-email")
    reset_password_link: str = Field(default="https://eventorize-api-thanhlam.site/reset-password")

settings = Settings()
