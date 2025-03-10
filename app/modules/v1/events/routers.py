from core.schemas import CommonsDependencies, ObjectIdStr, PaginationParams, UrlStr
from fastapi import Depends, File, UploadFile
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import event_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/events"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/events", status_code=200, responses={200: {"model": schemas.PublicListResponse, "description": "Get events success"}})
    async def get_all(self, pagination: PaginationParams = Depends()):
        search_in = ["title"]
        results = await event_controllers.get_all(
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
        return schemas.PublicListResponse(**results)

    @router.get("/events/{_id}", status_code=200, responses={200: {"model": schemas.PublicResponse, "description": "Get event success"}})
    async def get_detail(self, _id: ObjectIdStr, fields: str = None):
        results = await event_controllers.get_by_id(_id=_id, fields_limit=fields, commons=self.commons)
        if fields:
            return results
        return schemas.PublicResponse(**results)

    @router.post("/events", status_code=201, responses={201: {"model": schemas.Response, "description": "Create event success"}})
    async def create(self, data: schemas.CreateRequest = Depends(schemas.CreateRequest.as_form), file: UploadFile = File(None)):
        result = await event_controllers.create(data=data, file=file, commons=self.commons)
        return schemas.Response(**result)

    @router.put("/events/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Update event success"}})
    async def edit(self, _id: ObjectIdStr, data: schemas.EditRequest):
        results = await event_controllers.edit(_id=_id, data=data, commons=self.commons)
        return schemas.Response(**results)

    @router.put("/events/{_id}/thumbnail", status_code=200, responses={200: {"model": schemas.Response, "description": "Update event's thumbnail success"}})
    async def edit_thumbnail(self, _id: ObjectIdStr, file: UploadFile = File(None), image_url: UrlStr = None):
        results = await event_controllers.edit_thumbnail(_id=_id, file=file, image_url=image_url, commons=self.commons)
        return schemas.Response(**results)

    @router.delete("/events/{_id}", status_code=204)
    async def delete(self, _id: ObjectIdStr):
        await event_controllers.soft_delete_by_id(_id=_id, commons=self.commons)
