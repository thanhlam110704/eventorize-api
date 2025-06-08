from datetime import datetime
from typing import List, Optional

from core.schemas import ObjectIdStr, EmailStr, PhoneStr
from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    event_id: ObjectIdStr
    user_id: ObjectIdStr
    


class Response(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    event_id: str
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]