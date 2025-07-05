from utils import http_client
from .exceptions import ErrorCode as LocationErrorCode

class LocationApi:
    def __init__(self) -> None:
        self.url = "https://vn-public-apis.fpo.vn/"
        self.headers = {
            "Accept": "application/json"
        }

    async def get_provinces(self):
        url = f"{self.url}provinces/getAll?limit=-1"
        response = await http_client.get(url=url, headers=self.headers)
        response_data = response.json()
        province_list = response_data["data"]["data"]
        if not isinstance(province_list, list):
            raise LocationErrorCode.UnableToFetchData(url)
        return [
            {
                "name": item["name_with_type"],
                "code": int(item["code"]), 
                "division_type": item["type"],
                "codename": item["slug"],
            }
            for item in province_list
            if isinstance(item, dict) and "name_with_type" in item
        ]

    async def get_districts(self, province_code):
        url = f"{self.url}districts/getByProvince?provinceCode={province_code}&limit=-1"
        response = await http_client.get(url=url, headers=self.headers)
        response_data = response.json()
        district_list = response_data["data"]["data"]
        if not isinstance(district_list, list):
            raise LocationErrorCode.UnableToFetchData(url)
        return {
            "districts": [
                {
                    "name": item["name_with_type"],
                    "code": int(item["code"]),
                    "division_type": item["type"],
                    "codename": item["slug"],
                    "province_code": int(province_code)
                }
                for item in district_list
                if isinstance(item, dict) and "name_with_type" in item
            ]
        }

    async def get_wards(self, district_code):
        url = f"{self.url}wards/getByDistrict?districtCode={district_code}&limit=-1"
        response = await http_client.get(url=url, headers=self.headers)
        response_data = response.json()
        ward_list = response_data["data"]["data"]
        if not isinstance(ward_list, list):
            raise LocationErrorCode.UnableToFetchData(url)
        return {
            "wards": [
                {
                    "name": item["name_with_type"],
                    "code": int(item["code"]),
                    "division_type": item["type"],
                    "codename": item["slug"],
                    "district_code": int(district_code)
                }
                for item in ward_list
                if isinstance(item, dict) and "name_with_type" in item
            ]
        }