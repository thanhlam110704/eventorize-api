from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def Forbidden():
        return CustomException(type="core/warning/forbidden", status=403, title="Forbidden.", detail="You do not have permission to access this resource.")

    @staticmethod
    def InvalidPasswordLength():
        return CustomException(type="auth/info/invalid-password-length", status=400, title="Invalid password length.", detail="The password must be at least 8 characters long.")

    @staticmethod
    def InvalidOtpLength():
        return CustomException(type="auth/info/invalid-otp-length", status=400, title="Invalid otp length.", detail="The otp must have 6 characters.")
