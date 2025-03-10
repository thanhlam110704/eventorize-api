from core.services import BaseServices
from db.engine import app_engine
from modules.v1.tickets.services import ticket_services

from . import models
from .crud import OrderItemsCRUD


class OrderItemServices(BaseServices):
    def __init__(self, service_name: str, crud: OrderItemsCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create(self, order_id, data, commons):
        results = []
        for order_item in data["order_items"]:
            order_item["order_id"] = order_id
            order_item["status"] = "pending"
            order_item["created_by"] = self.get_current_user(commons=commons)
            order_item["created_at"] = self.get_current_datetime()
            data_save = models.OrderItems(**order_item).model_dump()
            result = await self.save(data_save)
            results.append(result)
        return results

    async def accept(self, data, commons):
        await ticket_services.verify_available(ticket_id=data["ticket_id"], quantity=data["quantity"])
        data_save = {"status": "active"}
        result = await self.update_by_id(_id=data["_id"], data=data_save, commons=commons)
        await ticket_services.adjust_ticket_quantity(ticket_id=data["ticket_id"], quantity=data["quantity"])
        return [result]


order_item_crud = OrderItemsCRUD(database_engine=app_engine, collection="order_items")
order_item_services = OrderItemServices(service_name="order items", crud=order_item_crud)
