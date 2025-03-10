from datetime import datetime
from typing import List, Optional

from core.schemas import EmailStr, PhoneStr, UrlStr
from fastapi import Form
from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    name: str
    logo: Optional[UrlStr] = None
    email: EmailStr
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

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        logo: str = Form(None),
        email: EmailStr = Form(...),
        phone: str = Form(None),
        description: str = Form(None),
        country: str = Form(None),
        city: str = Form(None),
        district: str = Form(None),
        ward: str = Form(None),
        facebook: str = Form(None),
        twitter: str = Form(None),
        linkedin: str = Form(None),
        instagram: str = Form(None),
    ) -> "CreateRequest":
        return cls(
            name=name,
            logo=logo,
            email=email,
            phone=phone,
            description=description,
            country=country,
            city=city,
            district=district,
            ward=ward,
            facebook=facebook,
            twitter=twitter,
            linkedin=linkedin,
            instagram=instagram,
        )


class Response(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    logo: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    # Location
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    # Social
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None

    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]


class EditRequest(BaseModel):
    name: Optional[str] = None
    logo: Optional[UrlStr] = None
    email: Optional[EmailStr] = None
    phone: Optional[PhoneStr] = None
    description: Optional[str] = None
    # location
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    # social
    facebook: Optional[UrlStr] = None
    twitter: Optional[UrlStr] = None
    linkedin: Optional[UrlStr] = None
    instagram: Optional[UrlStr] = None
