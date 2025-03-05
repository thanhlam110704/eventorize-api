from utils import http_client

from .exceptions import ErrorCode as LocationErrorCode


class LocationApi:
    def __init__(self) -> None:
        self.url = "https://provinces.open-api.vn/api/"
        self.headers = {}

    async def get_provinces(self):
        url = f"{self.url}?depth=1"
        response = await http_client.get(url=url, headers=self.headers)
        response_data = response.json()
        if "detail" in response_data:
            raise LocationErrorCode.UnableToFetchData(url)
        return response_data

    async def get_districts(self, province_code):
        url = f"{self.url}p/{province_code}?depth=2"
        response = await http_client.get(url=url, headers=self.headers)
        response_data = response.json()
        if "detail" in response_data:
            raise LocationErrorCode.UnableToFetchData(url)
        return response_data

    async def get_wards(self, district_code):
        url = f"{self.url}d/{district_code}?depth=2"
        response = await http_client.get(url=url, headers=self.headers)
        response_data = response.json()
        if "detail" in response_data:
            raise LocationErrorCode.UnableToFetchData(url)
        return response_data
