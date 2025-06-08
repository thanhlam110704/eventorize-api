
from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine

from . import models, schemas

class FavoriteServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data["created_by"] = self.get_current_user(commons=commons)
        data["created_at"] = self.get_current_datetime()
        data_save = models.Favorites(**data).model_dump()
        return await self.save(data=data_save)

favorite_crud = BaseCRUD(database_engine=app_engine, collection="favorites")
favorite_services = FavoriteServices(service_name="favorites", crud=favorite_crud)
