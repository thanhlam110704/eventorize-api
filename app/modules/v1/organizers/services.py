from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine

from . import models, schemas

# from modules.v1.collaborators.services import collaborator_services


class OrganizerServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data["created_by"] = self.get_current_user(commons=commons)
        data["created_at"] = self.get_current_datetime()
        data_save = models.Organizers(**data).model_dump()
        result = await self.save(data=data_save)
        # create collaborator with role Owner
        # await collaborator_services.create_owner(organizer_id=result["_id"], commons=commons)
        return result

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        data["updated_by"] = self.get_current_user(commons=commons)
        data["updated_at"] = self.get_current_datetime()
        return await self.update_by_id(_id=_id, data=data)


organizer_crud = BaseCRUD(database_engine=app_engine, collection="organizers")
organizer_services = OrganizerServices(service_name="organizers", crud=organizer_crud)
