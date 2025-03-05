from core.schemas import CommonsDependencies, ObjectIdStr, PaginationParams, UrlStr
from fastapi import Depends, File, UploadFile
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import organizer_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/organizers"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/organizers", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get organizers success"}})
    async def get_all(self, pagination: PaginationParams = Depends()):
        search_in = ["name", "email"]
        results = await organizer_controllers.get_all(
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

    @router.get("/organizers/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Get organizer success"}})
    async def get_detail(self, _id: ObjectIdStr, fields: str = None):
        results = await organizer_controllers.get_by_id(_id=_id, fields_limit=fields, commons=self.commons)
        if fields:
            return results
        return schemas.Response(**results)

    @router.get("/home/organizers/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Get organizer success"}})
    async def get_detail_public(self, _id: ObjectIdStr, fields: str = None):
        results = await organizer_controllers.get_by_id(_id=_id, fields_limit=fields, commons=None)
        if fields:
            return results
        return schemas.Response(**results)

    @router.post("/organizers", status_code=201, responses={201: {"model": schemas.Response, "description": "Create organizer success"}})
    async def create(self, data: schemas.CreateRequest = Depends(schemas.CreateRequest.as_form), file: UploadFile = File(None)):
        result = await organizer_controllers.create(data=data, file=file, commons=self.commons)
        return schemas.Response(**result)

    @router.put("/organizers/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Update organizer success"}})
    async def edit(self, _id: ObjectIdStr, data: schemas.EditRequest):
        results = await organizer_controllers.edit(_id=_id, data=data, commons=self.commons)
        return schemas.Response(**results)

    @router.put("/organizers/{_id}/logo", status_code=200, responses={200: {"model": schemas.Response, "description": "Update organizer's logo success"}})
    async def edit_thumbnail(self, _id: ObjectIdStr, file: UploadFile = None, image_url: UrlStr = None):
        results = await organizer_controllers.edit_logo(_id=_id, file=file, image_url=image_url, commons=self.commons)
        return schemas.Response(**results)

    @router.delete("/organizers/{_id}", status_code=204)
    async def delete(self, _id: ObjectIdStr):
        await organizer_controllers.soft_delete_by_id(_id=_id, commons=self.commons)
