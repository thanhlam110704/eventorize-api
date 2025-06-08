from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices


from . import schemas
from .services import favorite_services


class FavoriteControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def create(self, event_id: str, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        data["event_id"] = event_id
        data["user_id"] = self.get_current_user(commons=commons)
        return await self.service.create(data=data, commons=commons)
    
    async def soft_delete_by_id(self, _id: str, commons: CommonsDependencies = None) -> None:
        await self.get_by_id(_id=_id, commons=commons)
        return await self.service.soft_delete_by_id(_id=_id, commons=commons)
    

favorite_controllers = FavoriteControllers(controller_name="favorites", service=favorite_services)