from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from fastapi import UploadFile
from modules.v1.organizers.controllers import organizer_controllers
from modules.v1.tickets.services import ticket_services
from partners.v1.cloudflare.r2 import r2_services
from utils import converter

from . import schemas
from .config import settings
from .exceptions import ErrorCode as EventErrorCode
from .services import event_services


class EventControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def is_active(self, _id, ignore_error=False, commons: CommonsDependencies = None):
        # get event and check if event is still active
        event = await event_controllers.get_by_id(_id=_id, commons=commons)
        current_time = self.service.get_current_datetime()

        if converter.convert_str_to_datetime(event["end_date"]) < current_time:
            if not ignore_error:
                raise EventErrorCode.EventAlreadyEnded(event["title"])
            return False
        return event

    async def create(self, data: schemas.CreateRequest, file: UploadFile = None, commons: CommonsDependencies = None) -> dict:
        data = data.model_dump()
        await organizer_controllers.get_by_id(_id=data["organizer_id"], commons=commons)
        if file is None and data["thumbnail"] is None:
            raise EventErrorCode.ImageOrFileRequired()
        if file and data["thumbnail"]:
            raise EventErrorCode.OnlyOneInputAllowed()
        if file and file.size > settings.maximum_thumbnail_file_size:
            raise EventErrorCode.FileTooLarge()

        if data["thumbnail"]:
            return await self.service.create(data=data, commons=commons)

        title = converter.convert_str_to_slug(data["title"])
        timestamp = self.service.get_current_timestamp()
        filename = f"{title}_{timestamp}.jpg"
        file_content = await file.read()
        await file.close()
        data["thumbnail"] = await r2_services.upload_file(filename=filename, file_content=file_content)
        return await self.service.create(data=data, commons=commons)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        data = data.model_dump(exclude_none=True)
        return await self.service.edit(_id=_id, data=data, commons=commons)

    async def get_event_title_by_id(self, _id: str, commons: CommonsDependencies = None) -> str:
        fields_limit = ["title"]
        event_data = await self.get_by_id(_id=_id, fields_limit=fields_limit, commons=commons)
        return event_data.get("title") if event_data else None

    async def edit_thumbnail(self, _id: str, file: UploadFile = None, image_url: str = None, commons: CommonsDependencies = None) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        if file is None and image_url is None:
            raise EventErrorCode.ImageOrFileRequired()
        if file and image_url:
            raise EventErrorCode.OnlyOneInputAllowed()
        if file and file.size > settings.maximum_thumbnail_file_size:
            raise EventErrorCode.FileTooLarge()

        data_update = {}
        if image_url:
            data_update["thumbnail"] = image_url
            return await self.service.edit(_id=_id, data=data_update, commons=commons)

        title = await self.get_event_title_by_id(_id=_id, commons=commons)
        title = converter.convert_str_to_slug(title)
        timestamp = self.service.get_current_timestamp()
        filename = f"{title}_{timestamp}.jpg"
        file_content = await file.read()
        await file.close()
        data_update["thumbnail"] = await r2_services.upload_file(filename=filename, file_content=file_content)
        return await self.service.edit(_id=_id, data=data_update, commons=commons)

    async def export_events(self, commons: CommonsDependencies = None) -> dict:
        data = await self.get_all(limit=self.max_record_limit, commons=commons)
        return await self.service.export_events(data=data["results"])

    async def soft_delete_by_id(self, _id: str, commons: CommonsDependencies = None) -> None:
        await self.get_by_id(_id=_id, commons=commons)
        tickets = await ticket_services.get_all_by_event_id(event_id=_id, commons=commons)
        if tickets["total_items"] > 0:
            raise EventErrorCode.EventHasTickets()
        return await self.service.soft_delete_by_id(_id=_id, commons=commons)


event_controllers = EventControllers(controller_name="events", service=event_services)
