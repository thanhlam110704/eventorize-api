from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine
from modules.v1.events.services import event_services
from modules.v1.orders.services import order_services
from users.services import user_services
from utils import converter


class DashboardServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def get_top_buyer(self, start_date: str, end_date: str, limit: int = 3):
        start_date_obj = converter.convert_str_to_datetime_by_format(datetime_str=start_date)
        end_date_obj = converter.convert_str_to_datetime_by_format(datetime_str=end_date)
        return await order_services.get_top_buyer(start_date=start_date_obj, end_date=end_date_obj, limit=limit)

    async def get_total_event(self, start_date: str, end_date: str):
        return await event_services.get_total_event(start_date=start_date, end_date=end_date)

    async def get_general_report(self, start_date: str, end_date: str):
        result = {}
        start_date_obj = converter.convert_str_to_datetime_by_format(datetime_str=start_date)
        end_date_obj = converter.convert_str_to_datetime_by_format(datetime_str=end_date)
        revenue = await order_services.get_revenue(start_date=start_date_obj, end_date=end_date_obj)
        total_order = await order_services.get_total_orders(start_date=start_date_obj, end_date=end_date_obj)
        total_buyers = await order_services.get_total_buyers(start_date=start_date_obj, end_date=end_date_obj)
        total_users = await user_services.get_total_users(start_date=start_date_obj, end_date=end_date_obj)
        total_event = await event_services.get_count_event(start_date=start_date, end_date=end_date)
        result["total_revenues"] = revenue["total_revenue"]
        result["total_orders"] = total_order["total_order"]
        result["total_buyers"] = total_buyers["total_buyers"]
        result["total_users"] = total_users["total_items"]
        result["total_events"] = total_event["total_events"]
        return result


dashboard_crud = BaseCRUD(database_engine=app_engine, collection="dashboards")
dashboard_services = DashboardServices(service_name="dashboards", crud=dashboard_crud)
