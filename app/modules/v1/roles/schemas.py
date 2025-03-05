from datetime import datetime
from typing import List, Literal, Optional

from core.schemas import ObjectIdStr
from modules.v1.role_permissions import schemas as permission_schemas
from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    parent_role_id: Optional[ObjectIdStr] = None
    user_type: str
    is_hidden: bool = False
    status: Literal["active", "inactive"]
    permissions: List[permission_schemas.CreateRequest]


class Response(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: Optional[str] = None
    parent_role_id: Optional[str] = None
    parent_role_name: Optional[str] = None
    user_type: str
    is_hidden: bool
    status: str
    permissions: List[permission_schemas.Response]
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]


class EditRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    user_type: Optional[str] = None
    is_hidden: Optional[bool] = None
    status: Optional[Literal["active", "inactive"]] = None
    permissions: Optional[List[permission_schemas.EditRequest]] = None
