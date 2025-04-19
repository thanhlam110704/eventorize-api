from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from modules.v1.events.controllers import event_controllers
from modules.v1.orders.controllers import order_controllers
from utils import converter

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

    async def verify_sale_dates(self, event_data, ticket_data):
        # Convert string dates to datetime objects for event data
        event_start = converter.convert_str_to_datetime_by_format(event_data["start_date"], "%Y-%m-%d %H:%M:%S")
        event_end = converter.convert_str_to_datetime_by_format(event_data["end_date"], "%Y-%m-%d %H:%M:%S")
        # Get datetime objects from ticket data (they're already datetime objects)
        sale_start = ticket_data["start_sale_date"]
        sale_end = ticket_data["end_sale_date"]
        sale_start = sale_start.replace(tzinfo=None)
        sale_end = sale_end.replace(tzinfo=None)
        # Check if sale dates are within event dates
        if sale_start < event_start:
            return False

        if sale_end > event_end:
            return False

        return True

    async def verify_not_owner(self, ticket_id: str, user_id: str):
        ticket = await self.get_by_id(_id=ticket_id)
        if ticket["created_by"] == user_id:
            raise TicketErrorCode.OwnerCannotBuyOwnTicket()
        return ticket

    async def buy_ticket(self, event_id: str, data: schemas.BuyRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump()
        user_id = self.get_current_user(commons)
        for order_item in data["order_items"]:
            await self.verify_not_owner(ticket_id=order_item["ticket_id"], user_id=user_id)
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
        event = await event_controllers.get_by_id(_id=event_id, commons=commons)
        valid = await self.verify_sale_dates(event_data=event, ticket_data=data)
        if not valid:
            raise TicketErrorCode.InvalidSaleDates()
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
