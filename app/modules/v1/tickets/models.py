from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel, model_validator

from .exceptions import ErrorCode as TicketErrorCode


class Tickets(BaseModel):
    event_id: ObjectIdStr
    title: str
    description: Optional[str] = None
    quantity: int
    start_sale_date: datetime
    end_sale_date: datetime
    price: int
    min_per_user: int
    max_per_user: int
    status: Literal["active", "sold out", "paused", "hidden"]
    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None

    @model_validator(mode="after")
    def check_logic_ticket(self) -> "Tickets":
        start = self.start_sale_date
        end = self.end_sale_date
        # Check the start date of the sale must be less than the end date of the sale
        if start > end:
            raise TicketErrorCode.InvalidDateOfSale()
        return self
