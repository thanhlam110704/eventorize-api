from auth.decorator import access_control
from core.schemas import CommonsDependencies, DateStr
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import dashboard_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/dashboard"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/dashboard/top-buyer", status_code=200, responses={200: {"model": schemas.TopBuyerResponse, "description": "Get top buyer success"}})
    @access_control(admin=True)
    async def get_top_buyer(self, start_date: DateStr, end_date: DateStr, limit: int = 3):
        results = await dashboard_controllers.get_top_buyer(start_date=start_date, end_date=end_date, limit=limit)
        return schemas.TopBuyerResponse(results=results)

    @router.get("/dashboard/total-event", status_code=200, responses={200: {"model": schemas.TotalEventResponse, "description": "Get total event success"}})
    @access_control(admin=True)
    async def get_total_event(self, start_date: DateStr, end_date: DateStr):
        results = await dashboard_controllers.get_total_event(start_date=start_date, end_date=end_date)
        return schemas.TotalEventResponse(**results)

    @router.get("/dashboard/general-report", status_code=200, responses={200: {"model": schemas.GeneralReportResponse, "description": "Get general report success"}})
    @access_control(admin=True)
    async def get_general_report(self, start_date: DateStr, end_date: DateStr):
        results = await dashboard_controllers.get_general_report(start_date=start_date, end_date=end_date)
        return schemas.GeneralReportResponse(**results)
