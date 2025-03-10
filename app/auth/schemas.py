from core.schemas import EmailStr
from pydantic import BaseModel, Field, field_validator
from users.config import settings

from .exceptions import ErrorCode as AuthErrorCode


class VerifyEmailRequest(BaseModel):
    email: EmailStr
    otp: str

    @field_validator("otp")
    @classmethod
    def check_the_length_of_otp(cls, v: str) -> str:
        if len(v) < settings.otp_length:
            raise AuthErrorCode.InvalidOtpLength()
        return v


class ResendVerificationEmailRequest(BaseModel):
    email: EmailStr


class ResendVerificationEmailResponse(BaseModel):
    status: str = Field(default="success", description="The status of the response.")
    message: str = Field(default="Verification email resent successfully.", description="The message of the response.")


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    status: str = Field(default="success", description="The status of the response.")
    message: str = Field(default="Password reset email sent.", description="The message of the response.")


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def check_the_minimum_length_of_the_password(cls, v: str) -> str:
        if len(v) < settings.minimum_length_of_the_password:
            raise AuthErrorCode.InvalidPasswordLength()
        return v

    @field_validator("otp")
    @classmethod
    def check_the_length_of_otp(cls, v: str) -> str:
        if len(v) < settings.otp_length:
            raise AuthErrorCode.InvalidOtpLength()
        return v


class ResetPasswordResponse(BaseModel):
    status: str = Field(default="success", description="The status of the response.")
    message: str = Field(default="Password reset successfully.", description="The message of the response.")
