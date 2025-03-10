from datetime import datetime
from typing import Optional

from core.schemas import DateTimeStr, ObjectIdStr, UrlStr
from pydantic import BaseModel


class Events(BaseModel):
    organizer_id: ObjectIdStr
    title: str
    thumbnail: Optional[UrlStr] = None
    description: str
    start_date: DateTimeStr
    end_date: DateTimeStr
    link: Optional[UrlStr] = None
    is_online: bool
    address: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    created_at: datetime
    created_by: Optional[ObjectIdStr]
    updated_at: datetime = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: datetime = None
    deleted_by: Optional[ObjectIdStr] = None
