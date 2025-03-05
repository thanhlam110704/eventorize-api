from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel


class Collaborators(BaseModel):
    user_id: ObjectIdStr
    organizer_id: Optional[ObjectIdStr] = None
    event_id: Optional[ObjectIdStr] = None
    role_id: ObjectIdStr
    status: Literal["pending", "accepted"]
    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
