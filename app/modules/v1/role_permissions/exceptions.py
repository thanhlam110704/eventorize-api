from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def NotFound(role_id: str, permission_id: str):
        return CustomException(
            type="role-permissions/warning/not-found",
            status=400,
            title="Not Found.",
            detail=f"Role permission with role_id {role_id} and permission_id {permission_id} could not be found.",
        )
