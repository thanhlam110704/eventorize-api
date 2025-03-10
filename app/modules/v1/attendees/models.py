from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr, EmailStr, PhoneStr, DateTimeStr
from pydantic import BaseModel


class Attendees(BaseModel):
    user_id: Optional[ObjectIdStr] = None 
    ticket_id: ObjectIdStr
    event_id: ObjectIdStr
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[PhoneStr] = None
    check_in: DateTimeStr = None
    check_out: DateTimeStr = None
    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
