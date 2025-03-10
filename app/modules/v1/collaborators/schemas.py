from datetime import datetime
from typing import List, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel, Field


class Response(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    organizer_id: Optional[str] = None
    event_id: Optional[str] = None
    role_id: str
    role: Optional[str] = None
    fullname: Optional[str] = None
    email: Optional[str] = None
    status: str
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]


class InviteRequest(BaseModel):
    user_id: ObjectIdStr
    role_id: ObjectIdStr
