from partners.v1.location.services import location_services


class LocationControllers:
    async def get_province(self):
        return await location_services.get_province()

    async def get_districts(self, province_code: str):
        return await location_services.get_districts(province_code=province_code)

    async def get_wards(self, district_code: str):
        return await location_services.get_wards(district_code=district_code)


location_controllers = LocationControllers()
