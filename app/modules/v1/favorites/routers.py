from core.schemas import CommonsDependencies, PaginationParams, ObjectIdStr
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import favorite_controllers
from users.controllers import user_controllers
router = InferringRouter(
    prefix="/v1",
    tags=["v1/favorites"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  

    @router.get("/favorites/my-events", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get user favorite events"}})
    async def get_my_favorite_events(self, pagination: PaginationParams = Depends()):
        current_user = user_controllers.get_current_user(commons=self.commons)
        results = await favorite_controllers.get_all_event_by_user(
            user_id=current_user,
            page=pagination.page,
            limit=pagination.limit,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            commons=self.commons
        )
        return schemas.ListResponse(**results)
    
    @router.post("/favorites/add-event/{event_id}", status_code=201, responses={201: {"model": schemas.Response, "description": "Create favorite success"}})
    async def create(self, event_id: ObjectIdStr):
        current_user = user_controllers.get_current_user(commons=self.commons)
        data = schemas.CreateRequest(event_id=event_id, user_id=current_user)
        result = await favorite_controllers.create(data=data, commons=self.commons)
        return schemas.Response(**result)
    
    @router.delete("/favorites/{_id}", status_code=204)
    async def delete(self, _id: ObjectIdStr):
        await favorite_controllers.soft_delete_by_id(_id=_id, commons=self.commons)
    
