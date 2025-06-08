from core.schemas import CommonsDependencies, PaginationParams, ObjectIdStr
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

    @router.get("/favorites", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get favorites success"}})
    async def get_all(self, pagination: PaginationParams = Depends()):
        search_in = ["event_id"]
        results = await favorite_controllers.get_all(
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            commons=self.commons,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)
    
    @router.post("/favorites", status_code=201, responses={201: {"model": schemas.Response, "description": "Create favorite success"}})
    async def create(self, data: schemas.CreateRequest):
        result = await favorite_controllers.create(data=data, commons=self.commons)
        return schemas.Response(**result)
    
    @router.delete("/favorites/{_id}", status_code=204)
    async def delete(self, _id: ObjectIdStr):
        await favorite_controllers.soft_delete_by_id(_id=_id, commons=self.commons)
    
