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

    async def add_event(self, event_id: str, commons: CommonsDependencies) -> dict:
        await self.check_event_exists(event_id=event_id)
        current_user = self.get_current_user(commons=commons)
        data = schemas.AddEventRequest(event_id=event_id, user_id=current_user)
        return await self.service.add_event(data=data, commons=commons)
    
    async def check_event_exists(self, event_id: str ):
        event = await event_services.get_by_id(_id=event_id)
        if not event:
            raise ErrorCode.NotFound(service_name="events", item=event_id)
    
    async def get_all_event_by_user(self, user_id:str,  page: int = 1, limit: int = 10, sort_by: str = "created_at", order_by: str = "desc",
        commons: CommonsDependencies = None) -> dict:
        return await self.service.get_all_event_by_user(
            user_id=user_id,
            page=page,
            limit=limit,
            sort_by=sort_by,
            order_by=order_by,
            commons=commons
        )
       
    async def remove_event(self, event_id: str, commons: CommonsDependencies) -> dict:
        current_user = self.get_current_user(commons=commons)
        return await self.service.remove_event(user_id=current_user, event_id=event_id, commons=commons)
    

favorite_controllers = FavoriteControllers(controller_name="favorites", service=favorite_services)