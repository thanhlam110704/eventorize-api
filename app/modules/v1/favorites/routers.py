from core.schemas import CommonsDependencies, ObjectIdStr
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import favorite_controllers
from .services import favorite_services
from users.controllers import user_controllers
from modules.v1.events.controllers import event_controllers
router = InferringRouter(
    prefix="/v1",
    tags=["v1/favorites"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  

    @router.get("/favorites/my-events", status_code=200, responses={200: {"model": schemas.Response, "description": "Get user favorite events"}})
    async def get_my_favorite_events(self):
        current_user = user_controllers.get_current_user(commons=self.commons)
        favorite = await favorite_controllers.get_by_field(
            data=current_user,
            field_name="user_id",
            ignore_error=True,
            commons=self.commons
        )

        if favorite is None:
            favorite = await favorite_services.create_favorite(
                user_id=current_user.id,
                commons=self.commons,
                event_id=None
            )

        result = schemas.Response(
            id=str(favorite["_id"]),
            user_id=favorite["user_id"],
            events=[
                event for event in [
                    await event_controllers.get_by_id(_id=event_id, commons=self.commons)
                    for event_id in favorite.get("list_event_id", [])
                ] if event is not None
            ],
            created_at=favorite["created_at"],
            created_by=favorite["created_by"],
            updated_at=favorite.get("updated_at"),
            updated_by=favorite.get("updated_by")
        )
        return result
       
    @router.post("/favorites/add-event/{event_id}", status_code=201, responses={201: {"model": schemas.Response, "description": "Create favorite success"}})
    async def add_event(self, event_id: ObjectIdStr):
        result = await favorite_controllers.add_event(event_id = event_id, commons=self.commons)
        return schemas.Response(**result)
    
    @router.delete("/favorites/remove-event/{event_id}")
    async def remove_event(self, event_id: ObjectIdStr):
        return await favorite_controllers.remove_event(event_id=event_id, commons=self.commons)
    
