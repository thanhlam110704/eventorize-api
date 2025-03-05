from typing import List

from pydantic import BaseModel


class ProvinceResponse(BaseModel):
    name: str
    code: int
    division_type: str
    codename: str


class ListProvinceResponse(BaseModel):
    results: List[ProvinceResponse]


class DistrictResponse(BaseModel):
    name: str
    code: int
    division_type: str
    codename: str
    province_code: int


class ListDistrictResponse(BaseModel):
    districts: List[DistrictResponse]


class WardResponse(BaseModel):
    name: str
    code: int
    division_type: str
    codename: str
    district_code: int


class ListWardResponse(BaseModel):
    wards: List[WardResponse]
