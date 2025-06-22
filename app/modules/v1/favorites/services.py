
from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine
from modules.v1.events.services import event_services
from core.exceptions import ErrorCode
from . import models, schemas

class FavoriteServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    
    async def add_event(self, data: schemas.AddEventRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        favorite = await self.get_by_field(data=data["user_id"],ignore_error=True, field_name="user_id", commons=commons)
        if favorite:
            list_event_id = favorite.get("list_event_id", [])
            if data["event_id"] in list_event_id:
                raise ErrorCode.Conflict(service_name=self.service_name, item=data["event_id"])
            
            updated_data = {
                "list_event_id": list_event_id + [data["event_id"]],
                "updated_at": self.get_current_datetime(),
                "updated_by": data["user_id"]
            }
            result = await self.update_by_id( _id=favorite["_id"], data=updated_data, commons=commons)
        else:
            result = await self.create_favorite(data=data, commons=commons)

        result["events"] = [
            await event_services.get_by_id(_id=event_id, commons=commons)
            for event_id in result.get("list_event_id", [])
        ]
        return result

    async def get_favorite(self, user_id: str, commons: CommonsDependencies) -> dict:
        favorite = await self.get_by_field(data=user_id, field_name="user_id", ignore_error=True, commons=commons)
        if favorite:
            return favorite
        
        add_event_request = schemas.AddEventRequest(user_id=user_id, event_id=None)
        return await self.create_favorite(data=add_event_request, commons=commons)
    

    async def create_favorite(self, data: schemas.AddEventRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        data_save = {
            "user_id": data["user_id"],
            "list_event_id": [data["event_id"]] if data["event_id"] else [], 
            "created_by": self.get_current_user(commons=commons),
            "created_at": self.get_current_datetime()
        }
        result = await self.save(data=models.Favorites(**data_save).model_dump())
        return result
    
    
    async def remove_event(self, data: schemas.AddEventRequest , commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        current_time = self.get_current_datetime()
        favorite = await self.get_by_field(data=data["user_id"], field_name="user_id", ignore_error=False, include_deleted=False, commons=commons)
        
        if data["event_id"] not in favorite.get("list_event_id", []):
            raise ErrorCode.NotFound(service_name=self.service_name, item=data["event_id"])
      
        updated_list_event_id = [eid for eid in favorite["list_event_id"] if eid != data["event_id"]]
        updated_data = {
            "list_event_id": updated_list_event_id,
            "updated_at": current_time,
            "updated_by": data["user_id"]
        }
      
        result = await self.update_by_id(_id=favorite["_id"], data=updated_data, ignore_error=False, commons=commons)
        result["events"] = [
            await event_services.get_by_id(_id=eid, commons=commons)
            for eid in updated_list_event_id
        ]
        return result

favorite_crud = BaseCRUD(database_engine=app_engine, collection="favorites")
favorite_services = FavoriteServices(service_name="favorites", crud=favorite_crud)
