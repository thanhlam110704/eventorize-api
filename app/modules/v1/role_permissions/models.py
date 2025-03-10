from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel


class RolePermissions(BaseModel):
    role_id: ObjectIdStr
    permission_id: ObjectIdStr
    # Explicit denial of the permission for this role
    is_denied: bool
    status: Literal["active", "inactive"]
    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
