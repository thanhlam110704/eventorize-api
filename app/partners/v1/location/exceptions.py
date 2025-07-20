from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def UnableToFetchData(endpoint: str):
        return CustomException(type="province-api/error/unable-fetch-data", status=400, title="Không tìm thấy dữ liệu.", detail=f"Không thể lấy dữ liệu từ điểm cuối: {endpoint}.")