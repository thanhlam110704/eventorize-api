from core.schemas import CommonsDependencies, ObjectIdStr, PaginationParams
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from modules.v1.orders import schemas as order_schemas

from . import schemas
from .controllers import ticket_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/tickets"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/home/event/{event_id}/tickets", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get tickets success"}})
    async def get_event_tickets(self, event_id: ObjectIdStr, pagination: PaginationParams = Depends()):
        search_in = ["title"]
        results = await ticket_controllers.get_event_tickets(
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            event_id=event_id,
            commons=self.commons,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)

    @router.get("/event/tickets", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get tickets success"}})
    async def get_all(self, pagination: PaginationParams = Depends()):
        search_in = ["title"]
        results = await ticket_controllers.get_all(
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

    @router.get("/event/{event_id}/tickets", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get tickets success"}})
    async def get_all_tickets_by_event(self, event_id: ObjectIdStr, pagination: PaginationParams = Depends()):
        search_in = ["title"]
        results = await ticket_controllers.get_all_tickets_by_event(
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            event_id=event_id,
            commons=self.commons,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)

    @router.get("/event/{event_id}/tickets/{ticket_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Get ticket success"}})
    async def get_detail(self, event_id: ObjectIdStr, ticket_id: ObjectIdStr, fields: str = None):
        results = await ticket_controllers.get_detail(ticket_id=ticket_id, event_id=event_id, fields=fields, commons=self.commons)
        if fields:
            return results
        return schemas.Response(**results)

    @router.post("/event/{event_id}/tickets", status_code=201, responses={201: {"model": schemas.Response, "description": "Register ticket success"}})
    async def create(self, event_id: ObjectIdStr, data: schemas.CreateRequest):
        result = await ticket_controllers.create(event_id=event_id, data=data, commons=self.commons)
        return schemas.Response(**result)

    @router.post("/event/{event_id}/tickets/checkout", status_code=201, responses={201: {"model": order_schemas.Response, "description": "Create items success"}})
    async def buy(self, event_id: ObjectIdStr, data: schemas.BuyRequest):
        result = await ticket_controllers.buy_ticket(event_id=event_id, data=data, commons=self.commons)
        return order_schemas.Response(**result)

    @router.put("/event/{event_id}/tickets/{ticket_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Update ticket success"}})
    async def edit(self, event_id: ObjectIdStr, ticket_id: ObjectIdStr, data: schemas.EditRequest):
        results = await ticket_controllers.edit(ticket_id=ticket_id, event_id=event_id, data=data, commons=self.commons)
        return schemas.Response(**results)

    @router.delete("/event/tickets/{_id}", status_code=204)
    async def delete(self, _id: ObjectIdStr):
        await ticket_controllers.soft_delete_by_id(_id=_id, commons=self.commons)
