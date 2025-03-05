from datetime import datetime
from typing import List, Optional

from modules.v1.order_items import schemas as order_items_schemas
from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    promotion_code: Optional[str] = None
    override_amount: Optional[float] = None
    order_items: List[dict]


class Response(BaseModel):
    id: str = Field(alias="_id")
    order_no: str
    status: str
    amount: int
    discount_amount: Optional[int] = None
    tax_rate: float
    vat_amount: float
    total_amount: float
    promotion_code: Optional[str] = None
    notes: Optional[str] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_phone: Optional[str] = None
    order_items: List[order_items_schemas.Response] = []
    created_at: datetime
    created_by: str


class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]


class DetailsResponse(Response):
    order_items: Optional[List[order_items_schemas.Response]] = None
