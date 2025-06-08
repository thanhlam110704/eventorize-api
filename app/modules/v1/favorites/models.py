from datetime import datetime
from typing import Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel


class Favorites(BaseModel):
    user_id: ObjectIdStr
    event_id: ObjectIdStr
    created_at: datetime
    created_by: Optional[ObjectIdStr]
    updated_at: datetime = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: datetime = None
    deleted_by: Optional[ObjectIdStr] = None