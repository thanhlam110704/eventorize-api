from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .data_type import ApiPathStr, ScopeStr


class CreateRequest(BaseModel):
    name: str
    scope: ScopeStr
    group: str
    api_path: ApiPathStr
    method: Literal["GET", "POST", "PUT", "DELETE"]
    status: Literal["active", "inactive"]
    description: Optional[str] = None


class Response(BaseModel):
    id: str = Field(alias="_id")
    name: str
    scope: str
    group: str
    api_path: str
    method: str
    status: str
    description: Optional[str] = None
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
    scope: Optional[ScopeStr] = None
    group: Optional[str] = None
    api_path: Optional[str] = None
    method: Optional[Literal["GET", "POST", "PUT", "DELETE"]] = None
    status: Optional[Literal["active", "inactive"]] = None
    description: Optional[str] = None
