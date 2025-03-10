from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from fastapi import UploadFile
from partners.v1.cloudflare.r2 import r2_services
from utils import converter

from . import schemas
from .config import settings
from .exceptions import ErrorCode as OrganizerErrorCode
from .services import organizer_services


class OrganizerControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def create(self, data: schemas.CreateRequest, file: UploadFile = None, commons: CommonsDependencies = None) -> dict:
        data = data.model_dump()
        if file is None and data["logo"] is None:
            raise OrganizerErrorCode.ImageOrFileRequired()
        if file and data["logo"]:
            raise OrganizerErrorCode.OnlyOneInputAllowed()
        if file and file.size > settings.maximum_logo_file_size:
            raise OrganizerErrorCode.FileTooLarge()

        if data["logo"]:
            return await self.service.create(data=data, commons=commons)

        name = converter.convert_str_to_slug(data["name"])
        timestamp = self.service.get_current_timestamp()
        filename = f"{name}_{timestamp}.jpg"
        file_content = await file.read()
        await file.close()
        data["logo"] = await r2_services.upload_file(filename=filename, file_content=file_content)
        return await self.service.create(data=data, commons=commons)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        data = data.model_dump(exclude_none=True)
        return await self.service.edit(_id=_id, data=data, commons=commons)

    async def get_name_organizer_by_id(self, _id: str, commons: CommonsDependencies = None) -> str:
        fields_limit = ["name"]
        organizer_data = await self.get_by_id(_id=_id, fields_limit=fields_limit, commons=commons)
        return organizer_data.get("name") if organizer_data else None

    async def edit_logo(self, _id: str, file: UploadFile = None, image_url: str = None, commons: CommonsDependencies = None) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        if file is None and image_url is None:
            raise OrganizerErrorCode.ImageOrFileRequired()
        if file and image_url:
            raise OrganizerErrorCode.OnlyOneInputAllowed()
        if file and file.size > settings.maximum_logo_file_size:
            raise OrganizerErrorCode.FileTooLarge()

        data_update = {}
        if image_url:
            data_update["logo"] = image_url
            return await self.service.edit(_id=_id, data=data_update, commons=commons)

        name = await self.get_name_organizer_by_id(_id=_id, commons=commons)
        name = converter.convert_str_to_slug(name)
        timestamp = self.service.get_current_timestamp()
        filename = f"{name}_{timestamp}.jpg"
        file_content = await file.read()
        await file.close()
        data_update["logo"] = await r2_services.upload_file(filename=filename, file_content=file_content)
        return await self.service.edit(_id=_id, data=data_update, commons=commons)


organizer_controllers = OrganizerControllers(controller_name="organizers", service=organizer_services)
