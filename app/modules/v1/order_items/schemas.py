from datetime import datetime

from core.schemas import ObjectIdStr
from pydantic import BaseModel, Field
from core.schemas import UrlStr


class CreateRequest(BaseModel):
    ticket_id: ObjectIdStr
    quantity: int
    price: float


class Response(BaseModel):
    id: str = Field(alias="_id")
    order_id: str
    ticket_id: str
    ticket_title: str
    event_id: str
    event_title: str
    event_thumbnail: UrlStr
    event_address: str 
    event_start_date: datetime
    event_end_date: datetime
    status: str
    quantity: int
    price: float
    created_at: datetime
    created_by: str
