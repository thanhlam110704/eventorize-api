from datetime import datetime
from typing import List, Optional

from core.schemas import ObjectIdStr, EmailStr, PhoneStr
from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    event_id: ObjectIdStr
    ticket_id: ObjectIdStr
    full_name: Optional[str] = None
    email: EmailStr
    phone: Optional[PhoneStr] = None


class Response(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    event_id: str
    ticket_id: str
    full_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
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
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[PhoneStr] = None
