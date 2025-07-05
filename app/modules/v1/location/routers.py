from core.schemas import CommonsDependencies
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import location_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/location"],
)

@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/locations/province", status_code=200, responses={200: {"model": schemas.ListProvinceResponse, "description": "Get items success"}})
    async def get_province(self):
        result = await location_controllers.get_province()
        return schemas.ListProvinceResponse(**result)

    @router.get("/locations/districts", status_code=200, responses={200: {"model": schemas.ListDistrictResponse, "description": "Get items success"}})
    async def get_districts(self, province_code: str):
        result = await location_controllers.get_districts(province_code=province_code)
        return schemas.ListDistrictResponse(**result)

    @router.get("/locations/wards", status_code=200, responses={200: {"model": schemas.ListWardResponse, "description": "Get items success"}})
    async def get_wards(self, district_code: str):
        result = await location_controllers.get_wards(district_code=district_code)
        return schemas.ListWardResponse(**result)