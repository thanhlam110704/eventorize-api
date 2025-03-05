from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def UnableToFetchData(endpoint: str):
        return CustomException(type="province-api/error/unable-fetch-data", status=400, title="Not Found.", detail=f"Cannot fetch data from endpoint: {endpoint}.")
