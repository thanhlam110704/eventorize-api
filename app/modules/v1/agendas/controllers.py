from bson import ObjectId
from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from modules.v1.events.controllers import event_controllers

from . import schemas
from .exceptions import ErrorCode as AgendaErrorCode
from .services import agenda_services


class AgendaControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def validate_input_time(self, input_start_time, input_end_time, event_id, commons: CommonsDependencies = None) -> None:
        # check input time
        event = await event_controllers.is_active(event_id, commons=commons)

        if not (event["start_date"] <= input_start_time <= event["end_date"]):
            raise AgendaErrorCode.StartTimeOutOfRange()
        if not (event["start_date"] <= input_end_time <= event["end_date"]):
            raise AgendaErrorCode.EndTimeOutOfRange()

    async def get_all(
        self,
        query: dict = None,
        search: str = None,
        search_in: list = None,
        page: int = 1,
        limit: int = 20,
        fields_limit: list | str = None,
        sort_by: str = "created_at",
        order_by: str = "desc",
        include_deleted: bool = False,
        commons: CommonsDependencies = None,
        event_id: str = None,
    ) -> dict:
        if query is None:
            query = {}
        if event_id:
            query.update({"event_id": event_id})
        return await super().get_all(query, search, search_in, page, limit, fields_limit, sort_by, order_by, include_deleted, commons)

    async def get_agenda_by_event_id_and_agenda_id(self, event_id: str, agenda_id: str, fields_limit: list | str = None, commons: CommonsDependencies = None) -> dict:
        # get event and check if event is still active
        # get agenda by agenda_id and event_id
        await event_controllers.get_by_id(_id=event_id, commons=commons)
        query = {"_id": ObjectId(agenda_id)}
        result = await self.get_all(query=query, fields_limit=fields_limit, commons=commons, event_id=event_id)
        if not result["results"]:
            raise AgendaErrorCode.NotFound(agenda_id=agenda_id, event_id=event_id)
        return result["results"][0]

    async def create(self, event_id: str, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        await self.validate_input_time(input_start_time=data.start_time, input_end_time=data.end_time, event_id=event_id, commons=commons)
        data = data.model_dump()
        data["event_id"] = event_id
        return await self.service.create(data=data, commons=commons)

    async def edit(self, event_id: str, agenda_id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        agenda = await self.get_agenda_by_event_id_and_agenda_id(event_id=event_id, agenda_id=agenda_id, commons=commons)

        if data.start_time and data.end_time:
            await self.validate_input_time(input_start_time=data.start_time, input_end_time=data.end_time, event_id=event_id, commons=commons)
        data = data.model_dump(exclude_none=True)
        return await self.service.edit(_id=agenda["_id"], data=data, commons=commons)

    async def soft_delete_by_id(self, event_id: str, agenda_id: str, ignore_error: bool = False, commons: CommonsDependencies = None) -> dict:
        await self.get_agenda_by_event_id_and_agenda_id(event_id=event_id, agenda_id=agenda_id, commons=commons)
        return await super().soft_delete_by_id(agenda_id, ignore_error, commons)


agenda_controllers = AgendaControllers(controller_name="agendas", service=agenda_services)
