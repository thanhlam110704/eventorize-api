from datetime import datetime
from typing import List, Optional

from core.schemas import DateTimeStr, ObjectIdStr, UrlStr
from fastapi import Form
from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    organizer_id: ObjectIdStr
    title: str
    thumbnail: Optional[UrlStr] = None
    description: Optional[str] = None
    link: Optional[UrlStr] = None
    start_date: DateTimeStr
    end_date: DateTimeStr
    is_online: bool
    address: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        organizer_id: str = Form(...),
        title: str = Form(...),
        thumbnail: str = Form(None),
        description: str = Form(None),
        link: str = Form(None),
        start_date: str = Form(...),
        end_date: str = Form(...),
        is_online: bool = Form(...),
        address: str = Form(None),
        district: str = Form(None),
        ward: str = Form(None),
        city: str = Form(None),
        country: str = Form(None),
    ) -> "CreateRequest":
        return cls(
            organizer_id=organizer_id,
            title=title,
            thumbnail=thumbnail,
            description=description,
            link=link,
            start_date=start_date,
            end_date=end_date,
            is_online=is_online,
            address=address,
            district=district,
            ward=ward,
            city=city,
            country=country,
        )


class PublicResponse(BaseModel):
    id: str = Field(alias="_id")
    organizer_id: str
    title: str
    thumbnail: Optional[UrlStr] = None
    description: str
    link: Optional[UrlStr] = None
    start_date: datetime
    end_date: datetime
    is_online: bool
    address: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class PublicListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[PublicResponse]


class Response(PublicResponse):
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
    title: Optional[str] = None
    thumbnail: Optional[UrlStr] = None
    description: Optional[str] = None
    link: Optional[UrlStr] = None
    start_date: Optional[DateTimeStr] = None
    end_date: Optional[DateTimeStr] = None
    is_online: Optional[bool] = None
    address: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
