from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from modules.v1.events.controllers import event_controllers
from modules.v1.orders.controllers import order_controllers

from . import schemas
from .exceptions import ErrorCode as TicketErrorCode
from .services import ticket_services


class TicketControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def verify_ticket(self, ticket_id: str, event_id: str):
        data_ticket = await self.get_by_id(_id=ticket_id)
        await event_controllers.get_by_id(_id=event_id)
        if data_ticket["event_id"] != event_id:
            raise TicketErrorCode.InvalidEventId()

    async def buy_ticket(self, event_id: str, data: schemas.BuyRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        for order_item in data["order_items"]:
            await self.verify_ticket(ticket_id=order_item["ticket_id"], event_id=event_id)
            await ticket_services.verify_date_sale(ticket_id=order_item["ticket_id"])
            await ticket_services.verify_available(ticket_id=order_item["ticket_id"], quantity=order_item["quantity"])
            await ticket_services.verify_limit(ticket_id=order_item["ticket_id"], quantity=order_item["quantity"])
            order_item["price"] = await ticket_services.get_ticket_price(ticket_id=order_item["ticket_id"])
        return await order_controllers.create(data=data, commons=commons)

    async def get_detail(self, ticket_id: str, event_id: str, fields: list | str, commons: CommonsDependencies) -> dict:
        await self.verify_ticket(ticket_id=ticket_id, event_id=event_id)
        return await self.get_by_id(_id=ticket_id, fields_limit=fields, commons=commons)

    async def create(self, event_id: str, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        await event_controllers.get_by_id(_id=event_id, commons=commons)
        return await self.service.create(data=data, event_id=event_id, commons=commons)

    async def edit(self, ticket_id: str, event_id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        await self.verify_ticket(ticket_id=ticket_id, event_id=event_id)
        data = data.model_dump(exclude_none=True)
        return await self.service.edit(_id=ticket_id, data=data, commons=commons)

    async def get_event_tickets(
        self, query=None, search=None, search_in=None, page=1, limit=20, fields_limit=None, sort_by="created_at", order_by="desc", include_deleted=False, event_id: str = None, commons=None
    ):
        query = {"event_id": event_id, "status": {"$in": ["active", "sold out"]}}
        return await super().get_all(query, search, search_in, page, limit, fields_limit, sort_by, order_by, include_deleted, commons)

    async def get_all_tickets_by_event(
        self, query=None, search=None, search_in=None, page=1, limit=20, fields_limit=None, sort_by="created_at", order_by="desc", include_deleted=False, event_id: str = None, commons=None
    ):
        query = {"event_id": event_id}
        return await super().get_all(query, search, search_in, page, limit, fields_limit, sort_by, order_by, include_deleted, commons)


ticket_controllers = TicketControllers(controller_name="tickets", service=ticket_services)
