from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from modules.v1.events.controllers import event_controllers
from modules.v1.organizers.controllers import organizer_controllers
from modules.v1.roles.controllers import role_controllers
from users.controllers import user_controllers

from . import schemas
from .exceptions import ErrorCode as CollaboratorErrorCode
from .services import collaborator_services


class CollaboratorControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def get_all_collaborator(self, _id, query, search, search_in, page, limit, fields_limit, sort_by, order_by, is_event, commons: CommonsDependencies) -> dict:
        if is_event:
            query["event_id"] = _id
        else:
            query["organizer_id"] = _id

        results = await super().get_all(query=query, search=search, search_in=search_in, page=page, limit=limit, fields_limit=fields_limit, sort_by=sort_by, order_by=order_by, commons=commons)
        for item in results["results"]:
            role = await role_controllers.get_by_id(_id=item["role_id"])
            user = await user_controllers.get_by_id(_id=item["user_id"])
            item["role"] = role["user_type"]
            item["fullname"] = user["fullname"]
            item["email"] = user["email"]
        return results

    async def check_exist(self, data):
        await user_controllers.get_by_id(_id=data["user_id"])
        await role_controllers.get_by_id(_id=data["role_id"])

    async def check_existing_collaborator(self, _id: str, data: schemas.InviteRequest, query_type: str) -> None:
        query = {"organizer_id": _id} if query_type == "organizer" else {"event_id": _id}
        query["user_id"] = data["user_id"]

        # Check if collaborator already invited or accepted
        results = await self.get_all(query=query)
        if results["results"]:
            status = results["results"][0].get("status")
            if status == "accepted":
                raise CollaboratorErrorCode.CollaboratorAlreadyAccepted()
            elif status == "pending":
                raise CollaboratorErrorCode.CollaboratorAlreadyInvited()

    async def invite_organizer(self, _id: str, data: schemas.InviteRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        # Check exist organizer
        await organizer_controllers.get_by_id(_id=_id, commons=commons)
        # Check exist user and role
        await self.check_exist(data=data)
        # Check if collaborator already invited or accepted for organizer
        await self.check_existing_collaborator(_id=_id, data=data, query_type="organizer")
        return await self.service.invite(_id=_id, data=data, is_event=False, commons=commons)

    async def invite_event(self, _id: str, data: schemas.InviteRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        # Check exist event
        await event_controllers.get_by_id(_id=_id, commons=commons)
        # Check exist user and role
        await self.check_exist(data=data)
        # Check if collaborator already invited or accepted for event
        await self.check_existing_collaborator(_id=_id, data=data, query_type="event")
        return await self.service.invite(_id=_id, data=data, is_event=True, commons=commons)

    async def accept(self, _id: str, commons: CommonsDependencies) -> dict:
        results = await self.get_by_id(_id=_id, commons=commons)
        if results["status"] == "accepted":
            raise CollaboratorErrorCode.CollaboratorAlreadyAccepted()
        return await self.service.accept(_id=_id, commons=commons)


collaborator_controllers = CollaboratorControllers(controller_name="collaborators", service=collaborator_services)
