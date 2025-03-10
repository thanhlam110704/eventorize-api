from datetime import datetime
from typing import List, Optional

from core.schemas import DateTimeStr
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self

from .exceptions import ErrorCode as AgendaErrorCode


class Validate(BaseModel):
    @model_validator(mode="after")
    def check_input_time(self) -> Self:
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise AgendaErrorCode.EndTimeAfterStartTime()
        elif self.start_time and self.end_time and self.start_time < self.end_time:
            return self
        elif not self.start_time and not self.end_time:
            return self
        else:
            raise AgendaErrorCode.CheckInputTime()


class CreateRequest(Validate):
    title: str
    description: Optional[str] = None
    start_time: DateTimeStr
    end_time: DateTimeStr


class PublicResponse(BaseModel):
    id: str = Field(alias="_id")
    event_id: str
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime


class Response(PublicResponse):
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


class PublicListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[PublicResponse]


class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]


class EditRequest(Validate):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[DateTimeStr] = None
    end_time: Optional[DateTimeStr] = None
