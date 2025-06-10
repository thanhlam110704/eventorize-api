from datetime import datetime
from typing import Optional,List

from core.schemas import ObjectIdStr
from pydantic import BaseModel


class Favorites(BaseModel):
    user_id: ObjectIdStr
    list_event_id: List[ObjectIdStr]
    created_at: datetime
    created_by: Optional[ObjectIdStr]
    updated_at: datetime = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: datetime = None
    deleted_by: Optional[ObjectIdStr] = None