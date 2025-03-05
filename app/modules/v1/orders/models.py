from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel, Field


class Orders(BaseModel):
    order_no: str = Field(..., description="Order number must be exactly 8 digits", pattern=r"^\d{8}$")
    status: Literal["active", "pending"]
    amount: int
    discount_amount: Optional[int] = None
    tax_rate: float
    vat_amount: float
    total_amount: float
    promotion_code: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
