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
    commons: CommonsDependencies = Depends(CommonsDependencies)

    @router.get("/events", status_code=200, responses={200: {"model": schemas.PublicListResponse, "description": "Get events success"}})
    async def get_all(self, pagination: PaginationParams = Depends(), date_filter: str = None, is_online: bool = None, city: str = None):
        search_in = ["title"]
        query = pagination.query or {}

        if is_online is not None:
            query["is_online"] = is_online
        if city is not None:
            query["city"] = city

        if date_filter is not None:
            result = await event_controllers.get_events_by_date_filter(
                date_filter=date_filter,
                is_online=is_online,
                city=city,
                page=pagination.page,
                limit=pagination.limit,
                commons=self.commons
            )
            return schemas.PublicListResponse(
                total_items=result["total_items"],
                total_page=result["total_page"],
                records_per_page=result["records_per_page"],
                results=[schemas.PublicResponse(**item) for item in result["results"]]
            )
        else:
            results = await event_controllers.get_all(
                query=query,
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
        
    @router.get("/organizer/{organizer_id}/events", status_code=200, responses={200: {"model": schemas.PublicListResponse, "description": "Get events by organizer success"}})
    async def get_events_by_organizer(self, organizer_id: ObjectIdStr, pagination: PaginationParams = Depends()):
        search_in = ["title"]
        results = await event_controllers.get_all_events_by_organizer(
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            organizer_id=organizer_id,
            commons=self.commons,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)


    @router.get("/events/export", status_code=200)
    async def export_events(self):
        return await event_controllers.export_events(commons=self.commons)

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