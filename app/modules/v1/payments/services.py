from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine


class PaymentServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)


payment_crud = BaseCRUD(database_engine=app_engine, collection="payments")
payment_services = PaymentServices(service_name="payments", crud=payment_crud)
