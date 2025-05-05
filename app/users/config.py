from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    default_admin_email: Optional[str] = None
    default_admin_password: Optional[str] = None
    minimum_length_of_the_password: int = Field(default=8)
    maximum_avatar_file_size: int = Field(default=5 * 1024 * 1024)  # default 5MB
    otp_length: int = Field(default=6)
    verification_token_expire_minutes: int = Field(default=3)
    max_reset_password_attempts: int = Field(default=3)
    reset_password_otp_expire_minutes: int = Field(default=3)
    max_verify_email_attempts: int = Field(default=3)

settings = Settings()
