from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def InvalidScopeFormat(scope: str):
        return CustomException(
            type="permissions/info/invalid-scope-format",
            status=400,
            title="Invalid scope format.",
            detail=f"The scope {scope} is invalid. The scope must be in the format 'group.action'. Example: 'users.read'.",
        )

    @staticmethod
    def InvalidApiPathFormat(path: str):
        return CustomException(
            type="permissions/info/invalid-api-path-format",
            status=400,
            title="Invalid API path format.",
            detail=f"The API path {path} is invalid. The API path must follow the format '/vX/module/...' and not end with a trailing slash. Example: '/v1/users'.",
        )
