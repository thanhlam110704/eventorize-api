from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def InvalidPasswordLength():
        return CustomException(type="users/info/invalid-password-length", status=400, title="Độ dài mật khẩu không hợp lệ.", detail="Mật khẩu phải có ít nhất 8 ký tự.")

    @staticmethod
    def FileTooLarge():
        return CustomException(type="users/info/file-too-large", status=413, title="Tệp quá lớn.", detail="Tệp tải lên vượt quá kích thước tối đa 5MB.")

    @staticmethod
    def ImageOrFileRequired():
        return CustomException(type="users/info/image-or-file-required", status=400, title="Yêu cầu hình ảnh hoặc tệp.", detail="Phải cung cấp 'image_url' hoặc 'file'.")

    @staticmethod
    def OnlyOneInputAllowed():
        return CustomException(type="users/info/only-one-input-allowed", status=400, title="Chỉ được cung cấp một đầu vào.", detail="Chỉ cung cấp một trong hai: 'image_url' hoặc 'file'.")

    @staticmethod
    def SSOIdMismatch():
        return CustomException(type="users/sso/invalid-sso", status=400, title="Thông tin SSO không hợp lệ.", detail="Thông tin đăng nhập SSO cung cấp không đúng.")

    @staticmethod
    def EmailAlreadyVerified():
        return CustomException(type="auth/error/email-already-verified", status=400, title="Email đã được xác minh.", detail="Địa chỉ email đã được xác minh.")

    @staticmethod
    def OTPRequiredBeforeReset():
        return CustomException(type="auth/otp/required", status=400, title="Yêu cầu OTP để đặt lại.", detail="Bạn phải yêu cầu OTP trước khi đặt lại mật khẩu.")

    @staticmethod
    def OTPAttemptsExceeded():
        return CustomException(
            type="auth/otp/max-attempts", status=400, title="Vượt quá số lần thử.", detail="Bạn đã vượt quá số lần thử xác minh OTP tối đa."
        )

    @staticmethod
    def OTPExpired():
        return CustomException(type="auth/otp/expired", status=400, title="OTP hết hạn.", detail="Mã OTP đã hết hạn.")

    @staticmethod
    def OTPInvalid():
        return CustomException(type="auth/otp/invalid", status=400, title="OTP không hợp lệ.", detail="Mã OTP bạn nhập không đúng.")

    @staticmethod
    def UserHasOrganizers():
        return CustomException(
            type="users/info/user-has-organizers", status=400, title="Người dùng có nhà tổ chức.", detail="Người dùng này đã tạo một hoặc nhiều nhà tổ chức."
        )

    @staticmethod
    def UserHasOrders():
        return CustomException(type="users/info/user-has-orders", status=400, title="Người dùng có đơn hàng.", detail="Người dùng này đã tạo một hoặc nhiều đơn hàng.")