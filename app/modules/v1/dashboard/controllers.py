from core.controllers import BaseControllers
from core.services import BaseServices

from .services import dashboard_services


class DashboardControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def get_top_buyer(self, start_date: str, end_date: str, limit: int = 3):
        return await self.service.get_top_buyer(start_date=start_date, end_date=end_date, limit=limit)

    async def get_total_event(self, start_date: str, end_date: str):
        return await self.service.get_total_event(start_date=start_date, end_date=end_date)

    async def get_general_report(self, start_date: str, end_date: str):
        return await self.service.get_general_report(start_date=start_date, end_date=end_date)


dashboard_controllers = DashboardControllers(controller_name="dashboard", service=dashboard_services)
