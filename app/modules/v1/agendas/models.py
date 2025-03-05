from datetime import datetime
from typing import Optional

from core.schemas import DateTimeStr, ObjectIdStr
from pydantic import BaseModel, model_validator
from typing_extensions import Self

from .exceptions import ErrorCode as AgendaErrorCode


class Agendas(BaseModel):
    event_id: ObjectIdStr
    title: str
    description: Optional[str] = None
    start_time: DateTimeStr
    end_time: DateTimeStr
    created_at: datetime
    created_by: ObjectIdStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None

    @model_validator(mode="after")
    def check_input_time(self) -> Self:
        if self.start_time >= self.end_time:
            raise AgendaErrorCode.EndTimeAfterStartTime()
        return self
