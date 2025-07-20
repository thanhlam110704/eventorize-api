from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def Forbidden():
        return CustomException(type="core/warning/forbidden", status=403, title="Truy cập bị cấm.", detail="Bạn không có quyền truy cập vào tài nguyên này.")

    @staticmethod
    def InvalidPasswordLength():
        return CustomException(type="auth/info/invalid-password-length", status=400, title="Độ dài mật khẩu không hợp lệ.", detail="Mật khẩu phải có ít nhất 8 ký tự.")

    @staticmethod
    def InvalidOtpLength():
        return CustomException(type="auth/info/invalid-otp-length", status=400, title="Độ dài OTP không hợp lệ.", detail="Mã OTP phải có 6 ký tự.")