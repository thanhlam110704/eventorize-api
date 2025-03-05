from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel

from .schemas import ApiPathStr, ScopeStr


class Permissions(BaseModel):
    name: str
    scope: ScopeStr
    group: str
    api_path: ApiPathStr
    method: Literal["GET", "POST", "PUT", "DELETE"]
    status: Literal["active", "inactive"]
    description: Optional[str] = None
    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
