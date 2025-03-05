from core.schemas import CommonsDependencies, ObjectIdStr, PaginationParams
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import collaborator_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/collaborators"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/collaborators/events/{event_id}", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get collaborators success"}})
    async def get_all_event(self, event_id: ObjectIdStr, pagination: PaginationParams = Depends()):
        search_in = ["name", "email"]  # need to change

        results = await collaborator_controllers.get_all_collaborator(
            _id=event_id,
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            is_event=True,
            commons=self.commons,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)

    @router.get("/collaborators/organizers/{organizer_id}", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get collaborators success"}})
    async def get_all_organizer(self, organizer_id: ObjectIdStr, pagination: PaginationParams = Depends()):
        search_in = ["name", "email"]  # need to change

        results = await collaborator_controllers.get_all_collaborator(
            _id=organizer_id,
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            is_event=False,
            commons=self.commons,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)

    @router.get("/collaborators/{_id}", status_code=200, responses={200: {"model": schemas.Response, "description": "Get collaborator success"}})
    async def get_detail(self, _id: ObjectIdStr, fields: str = None):
        results = await collaborator_controllers.get_by_id(_id=_id, fields_limit=fields, commons=self.commons)
        if fields:
            return results
        return schemas.Response(**results)

    @router.post("/collaborators/organizers/{organizer_id}/invite", status_code=201, responses={201: {"model": schemas.Response, "description": "Create collaborator success"}})
    async def invite_organizer(self, organizer_id: ObjectIdStr, data: schemas.InviteRequest):
        result = await collaborator_controllers.invite_organizer(_id=organizer_id, data=data, commons=self.commons)
        return schemas.Response(**result)

    @router.post("/collaborators/events/{event_id}/invite", status_code=201, responses={201: {"model": schemas.Response, "description": "Create collaborator success"}})
    async def invite_event(self, event_id: ObjectIdStr, data: schemas.InviteRequest):
        result = await collaborator_controllers.invite_event(_id=event_id, data=data, commons=self.commons)
        return schemas.Response(**result)

    @router.post("/collaborators/{collaborator_id}/accept", status_code=201, responses={201: {"model": schemas.Response, "description": "Create collaborator success"}})
    async def accept(self, collaborator_id: ObjectIdStr):
        result = await collaborator_controllers.accept(_id=collaborator_id, commons=self.commons)
        return schemas.Response(**result)

    @router.delete("/collaborators/{_id}", status_code=204)
    async def delete(self, _id: ObjectIdStr):
        await collaborator_controllers.soft_delete_by_id(_id=_id, commons=self.commons)
