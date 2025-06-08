
from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine
from modules.v1.events.services import event_services
from . import models, schemas

class FavoriteServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data["created_by"] = self.get_current_user(commons=commons)
        data["created_at"] = self.get_current_datetime()
        data_save = models.Favorites(**data).model_dump()
        result = await self.save(data=data_save)
        event = await event_services.get_by_id(_id=data["event_id"], commons=commons)
        result["event"] = event
        return result
    
    async def get_all_event_by_user(self,user_id: str, page: int = 1, limit: int = 10, sort_by: str = "created_at", order_by: str = "desc",
        commons: CommonsDependencies = None) -> dict:
        query = {
            "user_id": user_id,
            "deleted_at": None
        }

        results = await super().get_all(
            query=query,
            page=page,
            limit=limit,
            sort_by=sort_by,
            order_by=order_by,
            commons=commons
        )

        for favorite in results["results"]:
            event = await event_services.get_by_id(
                _id=favorite.get("event_id"),
                commons=commons
            )
            favorite["event"] = event 

        return results


favorite_crud = BaseCRUD(database_engine=app_engine, collection="favorites")
favorite_services = FavoriteServices(service_name="favorites", crud=favorite_crud)
