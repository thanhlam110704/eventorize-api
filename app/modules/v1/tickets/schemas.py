from datetime import datetime
from typing import List, Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self

from .exceptions import ErrorCode as TicketErrorCode


class BaseValidateTicket(BaseModel):
    @model_validator(mode="after")
    def check_logic_ticket(self) -> Self:
        start = self.start_sale_date
        end = self.end_sale_date
        max = self.max_per_user
        min = self.min_per_user
        quantity = self.quantity
        # Check the max must be from better than or equal 0 and less than or equal 100
        if max <= 0 or max > 100:
            raise TicketErrorCode.InvalidMaxQuantity()
        # Check the min must be from better than or equal 0 and less than or equal 100
        if min <= 0 or min > 100:
            raise TicketErrorCode.InvalidMinQuantity()
        # Check the start date of the sale must be less than the end date of the sale
        if start > end:
            raise TicketErrorCode.InvalidDateOfSale()
        # Check minimum must be less than maximum
        if max < min:
            raise TicketErrorCode.InvalidMaxMin()
        # Check function the available quantity must be greater than or equal to the minimum quantity the user can purchase
        if quantity < min:
            raise TicketErrorCode.InvalidMiniumQuantity()
        return self


class CreateOrderRequest(BaseModel):
    ticket_id: ObjectIdStr
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    notes: Optional[str] = None


class BuyRequest(BaseModel):
    promotion_code: Optional[str] = None
    override_amount: Optional[float] = None
    order_items: List[CreateOrderRequest]


class CreateRequest(BaseValidateTicket):
    title: str
    description: Optional[str] = None
    quantity: int = Field(..., gte=0, description="Quantity must be greater than 0")
    start_sale_date: datetime
    end_sale_date: datetime
    price: int = Field(..., gte=0, description="Price must be greater than 0")
    status: Literal["active", "sold out", "paused", "hidden"]
    min_per_user: int
    max_per_user: int


class Response(BaseModel):
    id: str = Field(alias="_id")
    event_id: ObjectIdStr
    title: str
    description: Optional[str] = None
    quantity: int
    start_sale_date: datetime
    end_sale_date: datetime
    price: int
    min_per_user: int
    max_per_user: int
    status: str
    created_at: datetime
    created_by: str


class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]


class EditRequest(BaseValidateTicket):
    title: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = Field(None, gte=0, description="Quantity must be greater than 0")
    start_sale_date: Optional[datetime] = None
    end_sale_date: Optional[datetime] = None
    price: Optional[int] = Field(None, gte=0, description="Price must be greater than 0")
    min_per_user: Optional[int] = None
    max_per_user: Optional[int] = None
    status: Optional[Literal["active", "sold out", "paused", "hidden"]] = None

    @model_validator(mode="after")
    def check_logic_ticket(self) -> Self:
        start = self.start_sale_date
        end = self.end_sale_date
        max = self.max_per_user
        min = self.min_per_user
        quantity = self.quantity

        # Chỉ kiểm tra nếu các giá trị không phải là None
        if max is not None and (max <= 0 or max > 100):
            raise TicketErrorCode.InvalidMaxQuantity()

        if min is not None and (min <= 0 or min > 100):
            raise TicketErrorCode.InvalidMinQuantity()

        if start is not None and end is not None and start > end:
            raise TicketErrorCode.InvalidDateOfSale()

        if max is not None and min is not None and max < min:
            raise TicketErrorCode.InvalidMaxMin()

        if quantity is not None and min is not None and quantity < min:
            raise TicketErrorCode.InvalidMiniumQuantity()

        return self
