from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel


class OrderItems(BaseModel):
    order_id: ObjectIdStr
    ticket_id: ObjectIdStr
    status: Literal["active", "pending"]
    quantity: int
    price: float
    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[float] = None
    updated_by: Optional[str] = None
