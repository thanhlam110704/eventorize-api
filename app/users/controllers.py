from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from fastapi import UploadFile
from partners.v1.cloudflare.r2 import r2_services
from utils import converter, validator

from . import schemas
from .config import settings
from .exceptions import ErrorCode as UsersErrorCode
from .services import user_services


class UserControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def check_exist_email(self, email: str):
        normalized_email = converter.clean_email(email=email)
        result = await self.get_all(query={"email": {"$regex": normalized_email, "$options": "i"}})
        if result["total_items"] > 0:
            raise UsersErrorCode.Conflict(service_name="users", item=email)

    async def login(self, data: schemas.LoginRequest) -> dict:
        # Convert the Pydantic model 'data' to a dictionary
        data = data.model_dump()
        return await self.service.login(data=data)

    async def get_me(self, commons: CommonsDependencies, fields: str = None):
        current_user_id = self.get_current_user(commons=commons)
        return await self.get_by_id(_id=current_user_id, fields_limit=fields, commons=commons)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        # Check if that user id exists or not
        await self.get_by_id(_id=_id, commons=commons)
        data = data.model_dump(exclude_none=True)
        return await self.service.edit(_id=_id, data=data, commons=commons)

    async def get_user_fullname_by_id(self, _id: str, commons: CommonsDependencies = None) -> str:
        fields_limit = ["fullname"]
        user_data = await self.get_by_id(_id=_id, fields_limit=fields_limit, commons=commons)
        return user_data.get("fullname") if user_data else None

    async def edit_avatar(self, _id: str, file: UploadFile = None, image_url: str = None, commons: CommonsDependencies = None) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        if file is None and image_url is None:
            raise UsersErrorCode.ImageOrFileRequired()
        if file and image_url:
            raise UsersErrorCode.OnlyOneInputAllowed()
        if file and file.size > settings.maximum_avatar_file_size:
            raise UsersErrorCode.FileTooLarge()

        data_update = {}
        if image_url:
            data_update["avatar"] = image_url
            return await self.service.edit(_id=_id, data=data_update, commons=commons)

        fullname = await self.get_user_fullname_by_id(_id=_id, commons=commons)
        fullname = converter.convert_str_to_slug(fullname)
        timestamp = self.service.get_current_timestamp()
        filename = f"{fullname}_{timestamp}.jpg"
        file_content = await file.read()
        await file.close()
        data_update["avatar"] = await r2_services.upload_file(filename=filename, file_content=file_content)
        return await self.service.edit(_id=_id, data=data_update, commons=commons)

    async def get_by_email(self, email: str, ignore_error: bool = False) -> dict:
        return await self.service.get_by_email(email=email, ignore_error=ignore_error)

    async def _after_register(self, user: dict, is_register_with_sso: bool = False) -> dict:
        # Send a verification email to the user.
        if is_register_with_sso is False:
            await self.service.send_verification_email(user_id=user["_id"], email=user["email"], fullname=user["fullname"])
        return user

    async def register(self, data: schemas.RegisterRequest) -> dict:
        # Convert the Pydantic model 'data' to a dictionary
        data = data.model_dump()
        # Check if the email already exists
        await self.check_exist_email(email=data["email"])
        new_user = await self.service.register(data=data)
        return await self._after_register(user=new_user, is_register_with_sso=False)

    async def register_with_google(self, fullname: str, email: str, google_id: str, avatar: str) -> dict:
        new_user = await self.service.register_with_google(fullname=fullname, email=email, google_id=google_id, avatar=avatar)
        return await self._after_register(user=new_user, is_register_with_sso=True)

    async def single_sign_on_with_google(self, data: schemas.GoogleSSORequest) -> dict:
        data = data.model_dump()
        user = await self.get_by_email(email=data["email"], ignore_error=True)
        if user is None:
            new_user = await self.register_with_google(fullname=data["display_name"], email=data["email"], google_id=data["id"], avatar=data["picture"])
            return new_user
        user = await self.service.login_with_google(email=data["email"], google_id=data["id"])
        return user

    async def send_verification_email(self, commons: CommonsDependencies) -> None:
        current_user_id = self.get_current_user(commons=commons)
        # Fetch user and check token in the database
        user = await user_controllers.get_by_id(_id=current_user_id, commons=commons)
        if user.get("is_verified"):
            raise UsersErrorCode.EmailAlreadyVerified()
        # Send verification email
        await self.service.send_verification_email(user_id=user["_id"], email=user["email"], fullname=user["fullname"])

    async def send_reset_password_email(self, user_id: str, email: str, fullname: str) -> None:
        await self.service.send_reset_password_email(user_id=user_id, email=email, fullname=fullname)

    async def verify_reset_password_otp(self, email: str, otp: str) -> None:
        # Fetch user by email
        user = await self.get_by_email(email=email, ignore_error=True)
        # Silent return if user doesn't exist (security best practice)
        if not user:
            return
        # Check if OTP exists
        if not user.get("reset_password_otp"):
            raise UsersErrorCode.OTPRequiredBeforeReset()
        # Check attempt limits
        if user.get("reset_password_attempts", 0) >= settings.max_reset_password_attempts:
            raise UsersErrorCode.OTPAttemptsExceeded()
        # Check OTP expiration
        if validator.is_expired(user.get("reset_password_otp_expire")):
            raise UsersErrorCode.OTPExpired()
        # Verify OTP
        if otp != user.get("reset_password_otp"):
            await self.service.increment_reset_password_attempts(user_id=user["_id"])
            raise UsersErrorCode.OTPInvalid()

    async def reset_password(self, email: str, password: str) -> None:
        # Fetch user by email
        user = await self.get_by_email(email=email)
        # Reset password
        await self.service.update_password(user_id=user["_id"], password=password)

    async def verify_email(self, email: str, otp: str) -> dict:
        # Fetch user by email
        user = await self.get_by_email(email=email)
        # Check if user is already verified
        if user.get("is_verified"):
            raise UsersErrorCode.EmailAlreadyVerified()
        # Check attempt limits
        if user.get("verify_email_otp_attempts", 0) >= settings.max_verify_email_attempts:
            raise UsersErrorCode.OTPAttemptsExceeded()
        # Check OTP expiration
        if validator.is_expired(user.get("verify_email_otp_expire")):
            raise UsersErrorCode.OTPExpired()
        # Verify OTP
        if otp != user.get("verify_email_otp"):
            await self.service.increment_verify_email_attempts(user_id=user["_id"])
            raise UsersErrorCode.OTPInvalid()
        return await self.service.verify_email(user_id=user["_id"])


user_controllers = UserControllers(controller_name="users", service=user_services)
