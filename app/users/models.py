from datetime import datetime
from typing import Literal, Optional

from core.schemas import EmailStr, ObjectIdStr, PhoneStr, UrlStr
from pydantic import BaseModel


class Users(BaseModel):
    fullname: str
    email: EmailStr
    position: Optional[str] = None
    phone: Optional[PhoneStr] = None
    avatar: Optional[UrlStr] = None
    company: Optional[str] = None
    # Location
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    # Social
    facebook: Optional[UrlStr] = None
    twitter: Optional[UrlStr] = None
    linkedin: Optional[UrlStr] = None
    instagram: Optional[UrlStr] = None
    # Password is optional because it is none when the user is created by SSO (Single Sign-On)
    password: Optional[bytes] = None
    google_id: Optional[str] = None
    github_id: Optional[str] = None
    is_verified: bool = False
    reset_password_otp: Optional[str] = None
    reset_password_otp_expire: Optional[datetime] = None
    reset_password_attempts: Optional[int] = None
    verify_email_otp: Optional[str] = None
    verify_email_otp_expire: Optional[datetime] = None
    verify_email_otp_attempts: Optional[int] = None
    type: Literal["admin", "user"]
    created_at: datetime
    created_by: Optional[ObjectIdStr] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
