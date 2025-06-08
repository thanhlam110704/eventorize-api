from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from core.exceptions import ErrorCode 


from . import schemas
from .services import favorite_services
from modules.v1.events.services import event_services


class FavoriteControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        await self.check_exist_event(event_id=data["event_id"], user_id=data["user_id"])
        return await self.service.create(data=data, commons=commons)
    
    async def check_exist_event(self, event_id: str, user_id: str):
        result = await self.get_all(query={"event_id": event_id, "user_id": user_id})
        event = await event_services.get_by_id(_id=event_id)
        if result["total_items"] > 0:
            raise ErrorCode.Conflict(service_name="favorites", item=event["title"])
    
    async def get_all_event_by_user(self, user_id: str, page: int = 1, limit: int = 10, sort_by: str = "created_at", order_by: str = "desc",
        commons: CommonsDependencies = None) -> dict:
        return await self.service.get_all_event_by_user(user_id=user_id, page=page, limit=limit, sort_by=sort_by, order_by=order_by, commons=commons)
       
    async def soft_delete_by_id(self, _id: str, commons: CommonsDependencies = None) -> None:
        await self.get_by_id(_id=_id, commons=commons)
        return await self.service.soft_delete_by_id(_id=_id, commons=commons)
    

favorite_controllers = FavoriteControllers(controller_name="favorites", service=favorite_services)