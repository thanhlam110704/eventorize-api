from auth.decorator import access_control
from core.schemas import CommonsDependencies, ObjectIdStr, PaginationParams
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import role_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/roles"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/roles", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get roles success"}})
    @access_control(admin=True)
    async def get_all(self, pagination: PaginationParams = Depends()):
        search_in = ["name"]
        results = await role_controllers.get_all(
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

    @router.get("/roles/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Get role success"}})
    @access_control(admin=True)
    async def get_detail(self, _id: ObjectIdStr, fields: str = None):
        results = await role_controllers.get_by_id(_id=_id, fields_limit=fields, commons=self.commons)
        if fields:
            return results
        return schemas.Response(**results)

    @router.post("/roles", status_code=201, responses={201: {"model": schemas.Response, "description": "Create role success"}})
    @access_control(admin=True)
    async def create(self, data: schemas.CreateRequest):
        result = await role_controllers.create(data=data, commons=self.commons)
        return schemas.Response(**result)

    @router.put("/roles/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Update role success"}})
    @access_control(admin=True)
    async def edit(self, _id: ObjectIdStr, data: schemas.EditRequest):
        results = await role_controllers.edit(_id=_id, data=data, commons=self.commons)
        return schemas.Response(**results)

    @router.delete("/roles/{_id}", status_code=204)
    @access_control(admin=True)
    async def delete(self, _id: ObjectIdStr):
        await role_controllers.soft_delete_by_id(_id=_id, commons=self.commons)
