from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from modules.v1.order_items.controllers import order_item_controllers
from utils import converter

from . import schemas
from .exceptions import ErrorCode as OrderErrorCode
from .services import order_services


class OrderControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def get_all(self, query, search, search_in, page, limit, fields_limit, sort_by, order_by, start_date, end_date, commons: CommonsDependencies) -> dict:
        if start_date and end_date:
            start_date_str = converter.convert_str_to_datetime_by_format(start_date)
            end_date_str = converter.convert_str_to_datetime_by_format(end_date)
            query["created_at"] = {"$gte": start_date_str, "$lte": end_date_str}
            del query["start_date"]
            del query["end_date"]
        results = await super().get_all(query=query, search=search, search_in=search_in, page=page, limit=limit, fields_limit=fields_limit, sort_by=sort_by, order_by=order_by, commons=commons)
        if not results:
            return None
        for result in results["results"]:
            query = {"order_id": result["_id"]}
            order_items = await order_item_controllers.get_all(query=query, page=1, limit=self.max_record_limit)
            result["order_items"] = order_items["results"]
        return results

    async def get_by_id(self, _id, fields_limit=None, ignore_error=False, include_deleted=False, commons=None):
        result = await super().get_by_id(_id, fields_limit, ignore_error, include_deleted, commons)
        if not result:
            return None
        query = {"order_id": result["_id"]}
        order_items = await order_item_controllers.get_all(query=query, page=1, limit=self.max_record_limit)
        result["order_items"] = order_items["results"]
        return result

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        order = await self.service.create(data=data, commons=commons)
        order_items = await order_item_controllers.create(order_id=order["_id"], data=data, commons=commons)
        order["order_items"] = order_items
        return order

    async def accept(self, order_id, commons):
        order = await self.service.get_by_id(order_id, commons=commons)
        if order["status"] == "active":
            raise OrderErrorCode.OrderAlreadyActive()
        order_items = await order_item_controllers.accept(order_id=order_id, commons=commons)
        result = await self.service.active(order_id=order_id, commons=commons)
        result["order_items"] = order_items
        return result

    async def soft_delete_by_id(self, _id, commons: CommonsDependencies = None):
        await self.service.soft_delete_by_id(_id, commons=commons)
        await order_item_controllers.soft_delete_by_order(_id, commons=commons)

    async def export_orders(self, start_date, end_date, commons: CommonsDependencies):
        query = {}
        if start_date and end_date:
            start_date_str = converter.convert_str_to_datetime_by_format(start_date)
            end_date_str = converter.convert_str_to_datetime_by_format(end_date)
            query["created_at"] = {"$gte": start_date_str, "$lte": end_date_str}
        data = await super().get_all(query=query, limit=self.max_record_limit, commons=commons)
        return await self.service.export_orders(data=data["results"])


order_controllers = OrderControllers(controller_name="orders controllers", service=order_services)
