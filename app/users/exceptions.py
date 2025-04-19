from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def InvalidPasswordLength():
        return CustomException(type="users/info/invalid-password-length", status=400, title="Invalid password length.", detail="The password must be at least 8 characters long.")

    @staticmethod
    def FileTooLarge():
        return CustomException(type="users/info/file-too-large", status=413, title="File too large.", detail="The uploaded file exceeds the maximum size of 5MB.")

    @staticmethod
    def ImageOrFileRequired():
        return CustomException(type="users/info/image-or-file-required", status=400, title="Image or File Required", detail="Either 'image_url' or 'file' must be provided.")

    @staticmethod
    def OnlyOneInputAllowed():
        return CustomException(type="users/info/only-one-input-allowed", status=400, title="Only One Input Allowed", detail="Provide only one of 'image_url' or 'file'.")

    @staticmethod
    def SSOIdMismatch():
        return CustomException(type="users/sso/invalid-sso", status=400, title="Invalid SSO Information", detail="The provided SSO credentials are invalid. Please try again.")

    @staticmethod
    def EmailAlreadyVerified():
        return CustomException(type="auth/error/email-already-verified", status=400, title="Email Already Verified.", detail="The email address has already been verified.")

    @staticmethod
    def OTPRequiredBeforeReset():
        return CustomException(type="auth/otp/required", status=400, title="OTP Required Before Reset", detail="You must request an OTP before resetting your password.")

    @staticmethod
    def OTPAttemptsExceeded():
        return CustomException(
            type="auth/otp/max-attempts", status=400, title="Maximum attempts exceeded.", detail="You have exceeded the maximum number of OTP verification attempts. Please request a new OTP."
        )

    @staticmethod
    def OTPExpired():
        return CustomException(type="auth/otp/expired", status=400, title="OTP expired.", detail="The OTP has expired. Please request a new one.")

    @staticmethod
    def OTPInvalid():
        return CustomException(type="auth/otp/invalid", status=400, title="Invalid OTP.", detail="The OTP you entered is incorrect. Please try again.")

    @staticmethod
    def UserHasOrganizers():
        return CustomException(
            type="users/info/user-has-organizers", status=400, title="User has organizers.", detail="This user has created one or more organizers. Please delete them first."
        )

    @staticmethod
    def UserHasOrders():
        return CustomException(type="users/info/user-has-orders", status=400, title="User has orders.", detail="This user has created one or more orders. Please delete them first.")
