from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from .exception import ErrorCode as AttendeeErrorCode

from . import schemas
from .services import attendee_services
from modules.v1.events.controllers import event_controllers
from modules.v1.tickets.controllers import ticket_controllers

class AttendeeControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data_ticket = await ticket_controllers.get_by_id(_id=data["ticket_id"], commons=commons)
        if data_ticket["event_id"] != data["event_id"]:
            raise AttendeeErrorCode.NotFoundEvent(item=data["event_id"])
        data = data.model_dump()
        return await self.service.create(data=data, commons=commons)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        data = data.model_dump(exclude_none=True)
        return await self.service.edit(_id=_id, data=data, commons=commons)

    async def attendees_check_in(self, _id: str, commons: CommonsDependencies) -> dict:
        data_attendee = await self.get_by_id(_id=_id, commons=commons)
        if data_attendee["check_in"] is not None:
            raise AttendeeErrorCode.AlreadyCheckIn()
        await event_controllers.is_active(data_attendee["event_id"])
        return await self.service.check_in(_id=_id, commons=commons)

    async def attendees_check_out(self, _id: str, commons: CommonsDependencies) -> dict:
        data_attendee = await self.get_by_id(_id=_id, commons=commons)
        if data_attendee["check_out"] is not None:
            raise AttendeeErrorCode.AlreadyCheckOut()
        return await self.service.check_out(_id=_id, commons=commons)
    

attendee_controllers = AttendeeControllers(controller_name="attendees", service=attendee_services)
