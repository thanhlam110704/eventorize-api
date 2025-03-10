from .api import LocationApi


class LocationServices:
    def __init__(self) -> None:
        self.location_api = LocationApi()

    async def get_province(self):
        result = {}
        result["results"] = await self.location_api.get_provinces()
        return result

    async def get_districts(self, province_code: str):
        return await self.location_api.get_districts(province_code=province_code)

    async def get_wards(self, district_code: str):
        return await self.location_api.get_wards(district_code=district_code)


location_services = LocationServices()
