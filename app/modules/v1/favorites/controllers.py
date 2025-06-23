from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from core.exceptions import ErrorCode 


from . import schemas
from .services import favorite_services
from modules.v1.events.services import event_services
from modules.v1.events.controllers import event_controllers


class FavoriteControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def get_my_favorite_events(self, commons: CommonsDependencies) -> dict:
        current_user = self.get_current_user(commons=commons)
        favorite = await self.service.get_favorite(user_id=current_user,commons=commons)
        return  {
            "_id":str(favorite["_id"]),
            "user_id":favorite["user_id"],
            "events":[
                await event_controllers.get_by_id(_id=event_id)
                for event_id in favorite.get("list_event_id", [])
            ],
            "created_at": favorite["created_at"],
            "created_by": favorite["created_by"],
            "updated_at": favorite.get("updated_at"),
            "updated_by": favorite.get("updated_by")
        }
        
    
    async def add_event(self, event_id: str, commons: CommonsDependencies) -> dict:
        await self.check_event_exists(event_id=event_id)
        current_user = self.get_current_user(commons=commons)
        data = schemas.AddEventRequest(event_id=event_id, user_id=current_user)
        return await self.service.add_event(data=data, commons=commons)
    
    async def check_event_exists(self, event_id: str ):
        event = await event_services.get_by_id(_id=event_id)
        if not event:
            raise ErrorCode.NotFound(service_name="events", item=event_id)
       
    async def remove_event(self, event_id: str, commons: CommonsDependencies) -> dict:
        current_user = self.get_current_user(commons=commons)
        data = schemas.AddEventRequest(event_id=event_id, user_id=current_user)
        return await self.service.remove_event(data=data, commons=commons)
    

favorite_controllers = FavoriteControllers(controller_name="favorites", service=favorite_services)