from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine

from . import models, schemas
from .exceptions import ErrorCode as TicketErrorCode


class TicketServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create(self, event_id: str, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data["event_id"] = event_id
        data["created_by"] = self.get_current_user(commons=commons)
        data["created_at"] = self.get_current_datetime()
        data_save = models.Tickets(**data).model_dump()
        return await self.save(data=data_save)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        data["updated_by"] = self.get_current_user(commons=commons)
        data["updated_at"] = self.get_current_datetime()
        return await self.update_by_id(_id=_id, data=data, commons=commons)

    async def verify_date_sale(self, ticket_id: str) -> dict:
        ticket = await self.get_by_id(_id=ticket_id)
        if ticket["start_sale_date"] > self.get_current_datetime():
            raise TicketErrorCode.TicketNotYetOnSale()
        if ticket["end_sale_date"] < self.get_current_datetime():
            raise TicketErrorCode.TicketExpired()

    async def verify_available(self, ticket_id: str, quantity: int) -> dict:
        ticket = await self.get_by_id(_id=ticket_id)
        if ticket["status"] == "sold out":
            raise TicketErrorCode.TicketSoldOut()
        if ticket["quantity"] < quantity:
            raise TicketErrorCode.TicketNotEnough()

    async def verify_limit(self, ticket_id: str, quantity: int) -> dict:
        ticket = await self.get_by_id(_id=ticket_id)
        if ticket["min_per_user"] > quantity:
            raise TicketErrorCode.InvalidMiniumQuantity()
        if ticket["max_per_user"] < quantity:
            raise TicketErrorCode.InvalidMaximumQuantity()

    async def adjust_ticket_quantity(self, ticket_id: str, quantity: int) -> dict:
        ticket = await self.get_by_id(_id=ticket_id)
        ticket["quantity"] -= quantity
        data_save = {"quantity": ticket["quantity"]}
        result = await self.update_by_id(_id=ticket_id, data=data_save)
        if result["quantity"] == 0:
            await self.update_by_id(_id=ticket_id, data={"status": "sold out"})

    async def get_ticket_price(self, ticket_id: str) -> dict:
        ticket = await self.get_by_id(_id=ticket_id)
        return ticket["price"]

    async def get_all_by_event_id(self, event_id: str, commons: CommonsDependencies = None) -> list:
        return await self.get_all(query={"event_id": event_id}, commons=commons)


ticket_crud = BaseCRUD(database_engine=app_engine, collection="tickets")
ticket_services = TicketServices(service_name="tickets", crud=ticket_crud)
