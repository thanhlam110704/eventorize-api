from typing import List, Optional

from pydantic import BaseModel, Field


class TopBuyerDetail(BaseModel):
    user_id: str
    user_name: str
    user_email: str
    orders: int
    total_amount: float


class TopBuyerResponse(BaseModel):
    results: Optional[List[TopBuyerDetail]] = None


class EventDetail(BaseModel):
    event_id: str = Field(alias="_id")
    title: str
    description: str
    start_date: str
    end_date: str


class TotalEventResponse(BaseModel):
    total_event_online: int
    total_event_offline: int
    list_event_online: List[EventDetail]
    list_event_offline: List[EventDetail]


class GeneralReportResponse(BaseModel):
    total_revenues: float
    total_orders: int
    total_buyers: int
    total_events: int
    total_users: int
