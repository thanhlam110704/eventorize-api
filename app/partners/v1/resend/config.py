from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    resend_api_key: Optional[str] = None
    host_email: str = Field(default="noreply@giapkun.site")
    sender_name: str = Field(default="Eventorize")
    verification_link: str = Field(default="https://eventorize.giapkun.site/verify-email")
    reset_password_link: str = Field(default="https://eventorize.giapkun.site/reset-password")

settings = Settings()
