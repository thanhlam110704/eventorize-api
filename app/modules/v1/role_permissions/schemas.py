from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    id: ObjectIdStr = Field(alias="_id")
    status: Literal["active", "inactive"]
    is_denied: bool


class EditRequest(BaseModel):
    id: ObjectIdStr = Field(alias="_id")
    status: Optional[Literal["active", "inactive"]] = None
    is_denied: Optional[bool] = None


class Response(BaseModel):
    id: str = Field(alias="permission_id")
    name: str
    scope: str
    group: str
    is_denied: bool
    status: str
    description: Optional[str] = None
    is_inherited_from_parent_role: bool
