from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel


class Roles(BaseModel):
    name: str
    description: Optional[str] = None
    # Reference to the parent role for inheritance
    parent_role_id: Optional[ObjectIdStr] = None
    # Type of user this role applies to (e.g., 'user', 'admin', 'merchant')
    user_type: str
    # Flag to hide the role from being used but still keep it in the system
    is_hidden: bool = False
    status: Literal["active", "inactive"]
    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
