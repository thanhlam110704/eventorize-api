from core.schemas import CommonsDependencies, ObjectIdStr, PaginationParams
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import agenda_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/agendas"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/events/{event_id}/agendas", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get agendas success"}})
    async def get_all_for_admin(self, event_id: ObjectIdStr, pagination: PaginationParams = Depends()):
        search_in = ["title"]
        results = await agenda_controllers.get_all(
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            commons=self.commons,
            event_id=event_id,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)

    @router.get("/home/events/{event_id}/agendas", status_code=200, responses={200: {"model": schemas.PublicListResponse, "description": "Get agendas success"}})
    async def get_all(self, event_id: ObjectIdStr, pagination: PaginationParams = Depends()):
        search_in = ["title"]
        results = await agenda_controllers.get_all(
            event_id=event_id,
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

    @router.get("/home/events/{event_id}/agendas/{agenda_id}", status_code=200, responses={200: {"model": schemas.PublicResponse, "description": "Get agendas success"}})
    async def get_detail(self, event_id: ObjectIdStr, agenda_id: ObjectIdStr, fields: str = None):
        results = await agenda_controllers.get_agenda_by_event_id_and_agenda_id(event_id=event_id, agenda_id=agenda_id, fields_limit=fields, commons=self.commons)
        if fields:
            return results
        return schemas.PublicResponse(**results)

    @router.post("/events/{event_id}/agendas", status_code=201, responses={201: {"model": schemas.Response, "description": "Create agenda success"}})
    async def create(self, event_id: ObjectIdStr, data: schemas.CreateRequest):
        result = await agenda_controllers.create(event_id=event_id, data=data, commons=self.commons)
        return schemas.Response(**result)

    @router.put("/events/{event_id}/agendas/{agenda_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Update agenda success"}})
    async def edit(self, event_id: ObjectIdStr, agenda_id: ObjectIdStr, data: schemas.EditRequest):
        results = await agenda_controllers.edit(event_id=event_id, agenda_id=agenda_id, data=data, commons=self.commons)
        return schemas.Response(**results)

    @router.delete("/events/{event_id}/agendas/{agenda_id}", status_code=204)
    async def delete(self, event_id: ObjectIdStr, agenda_id: ObjectIdStr):
        await agenda_controllers.soft_delete_by_id(event_id=event_id, agenda_id=agenda_id, commons=self.commons)
