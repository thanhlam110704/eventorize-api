from datetime import datetime
from typing import Optional

from core.schemas import EmailStr, ObjectIdStr, PhoneStr, UrlStr
from pydantic import BaseModel


class Organizers(BaseModel):
    name: str
    email: EmailStr
    logo: Optional[UrlStr] = None
    phone: Optional[PhoneStr] = None
    description: Optional[str] = None
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

    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
