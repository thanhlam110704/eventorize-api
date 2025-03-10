from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine
from modules.v1.roles.services import role_services

from . import models, schemas


class CollaboratorServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create_owner(self, organizer_id, commons: CommonsDependencies) -> dict:
        role_id = await role_services.get_owner_role_id()
        current_user = self.get_current_user(commons=commons)
        data = {}
        data["user_id"] = current_user
        data["organizer_id"] = organizer_id
        data["role_id"] = role_id
        data["status"] = "accepted"
        data["created_by"] = current_user
        data["created_at"] = self.get_current_datetime()
        data_save = models.Collaborators(**data).model_dump()
        return await self.save(data=data_save)

    async def invite(self, _id: str, data: schemas.InviteRequest, is_event: bool, commons: CommonsDependencies) -> dict:
        if is_event:
            data["event_id"] = _id
        else:
            data["organizer_id"] = _id
        data["status"] = "pending"
        data["created_by"] = self.get_current_user(commons=commons)
        data["created_at"] = self.get_current_datetime()
        data_save = models.Collaborators(**data).model_dump()
        result = await self.save(data=data_save)
        # Send email to user with collaborator_id
        return result

    async def accept(self, _id: str, commons: CommonsDependencies) -> dict:
        data = {}
        data["status"] = "accepted"
        data["updated_by"] = self.get_current_user(commons=commons)
        data["updated_at"] = self.get_current_datetime()
        return await self.update_by_id(_id=_id, data=data)


collaborator_crud = BaseCRUD(database_engine=app_engine, collection="collaborators")
collaborator_services = CollaboratorServices(service_name="collaborators", crud=collaborator_crud)
