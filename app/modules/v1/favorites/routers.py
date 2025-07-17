from core.schemas import CommonsDependencies, ObjectIdStr
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import favorite_controllers
router = InferringRouter(
    prefix="/v1",
    tags=["v1/favorites"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  

    @router.get("/favorites/my-events", status_code=200, responses={200: {"model": schemas.Response, "description": "Get user favorite events"}})
    async def get_my_favorite_events(self):
        result = await favorite_controllers.get_my_favorite_events(commons=self.commons)
        return schemas.Response(**result)
       
    @router.post("/favorites/add-event/{event_id}", status_code=201, responses={201: {"model": schemas.Response, "description": "Create favorite success"}})
    async def add_event(self, event_id: ObjectIdStr):
        result = await favorite_controllers.add_event(event_id = event_id, commons=self.commons)
        return schemas.Response(**result)
    
    @router.delete("/favorites/remove-event/{event_id}")
    async def remove_event(self, event_id: ObjectIdStr):
        return await favorite_controllers.remove_event(event_id=event_id, commons=self.commons)
    
