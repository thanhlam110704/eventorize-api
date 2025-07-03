from core.controllers import BaseControllers
from modules.v1.orders.controllers import order_controllers
from partners.v1.payos.api import payos_api

from .services import payment_services


class PaymentControllers(BaseControllers):
    def __init__(self, controller_name: str, service=None) -> None:
        super().__init__(controller_name, service)

    async def generate_qr(self, order_id: str):
        order = await order_controllers.get_by_id(order_id)
        result = await payos_api.create_payment_link(order_id=order_id, order_code=int(order["order_no"]), amount=order["total_amount"])
        return result
    
    async def get_payment_status(self, order_code: int):
        result = await payos_api.get_payment_information(order_code)
        return result


payment_controllers = PaymentControllers(controller_name="payments controllers", service=payment_services)
