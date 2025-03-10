from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices

from .services import order_item_services


class OrderItemControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def create(self, order_id, data, commons: CommonsDependencies = None) -> list:
        return await self.service.create(order_id=order_id, data=data, commons=commons)

    async def accept(self, order_id, commons: CommonsDependencies = None):
        result = await self.get_by_field(data=order_id, field_name="order_id", commons=commons)
        return await self.service.accept(data=result, commons=commons)

    async def soft_delete_by_order(self, order_id, commons: CommonsDependencies = None):
        query = {"order_id": order_id}
        order_items = await self.get_by_query(query=query, record_limit=self.max_record_limit, commons=commons)
        for order_item in order_items:
            await order_item_controllers.soft_delete_by_id(order_item["_id"], commons=commons)


order_item_controllers = OrderItemControllers(controller_name="order items controllers", service=order_item_services)
