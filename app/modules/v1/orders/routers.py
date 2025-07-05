from core.schemas import CommonsDependencies, DateStr, ObjectIdStr, PaginationParams
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import order_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/orders"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/orders", status_code=200, responses={200: {"model": schemas.ListResponse, "description": "Get orders success"}})
    async def get_all(self, pagination: PaginationParams = Depends(), start_date: DateStr = None, end_date: DateStr = None):
        search_in = ["user_name", "user_email", "user_phone", "order_no", "status"]
        results = await order_controllers.get_all(
            query=pagination.query,
            search=pagination.search,
            search_in=search_in,
            page=pagination.page,
            limit=pagination.limit,
            fields_limit=pagination.fields,
            sort_by=pagination.sort_by,
            order_by=pagination.order_by,
            start_date=start_date,
            end_date=end_date,
            commons=self.commons,
        )
        if pagination.fields:
            return results
        return schemas.ListResponse(**results)

    @router.get("/orders/export", status_code=200)
    async def export_orders(self, start_date: DateStr = None, end_date: DateStr = None):
        return await order_controllers.export_orders(start_date=start_date, end_date=end_date, commons=self.commons)

    @router.get("/orders/{_id}", status_code=200, responses={200: {"model": schemas.DetailsResponse, "description": "Get organizer success"}})
    async def get_detail(self, _id: ObjectIdStr, fields: str = None):
        results = await order_controllers.get_by_id(_id=_id, fields_limit=fields, commons=self.commons)
        if fields:
            return results
        return schemas.DetailsResponse(**results)

    @router.post("/orders/{_id}/accept", status_code=201, responses={201: {"model": schemas.Response, "description": "Accept items success"}})
    async def accept_order(self, _id: ObjectIdStr):
        result = await order_controllers.accept(order_id=_id, commons=self.commons)
        return schemas.Response(**result)

    @router.delete("/orders/{_id}", status_code=204)
    async def delete(self, _id: ObjectIdStr):
        await order_controllers.soft_delete_by_id(_id, commons=self.commons)
