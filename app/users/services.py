from typing import Any, Dict
from auth.services import authentication_services
from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine
from partners.v1.resend.services import user_mail_services
from utils import calculator, value

from . import models, schemas
from .config import settings
from .exceptions import ErrorCode as UserErrorCode


class UserServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def get_by_email(self, email: str, ignore_error: bool = False) -> dict | None:
        results = await self.get_by_field(data=email, field_name="email", ignore_error=ignore_error)
        return results if results else None
    
    async def delete_fields(self, _id: str, field_names: list[str]) -> None:
        await self.crud.delete_field_by_id(_id=_id, field_name=field_names)

    async def grant_admin(self, _id: str, commons: CommonsDependencies = None):
        data = {}
        data["type"] = value.UserRoles.ADMIN.value
        data["updated_at"] = self.get_current_datetime()
        data["updated_by"] = self.get_current_user(commons=commons)
        return await self.update_by_id(_id=_id, data=data)

    async def create_admin(self):
        user = await self.get_by_email(email=settings.default_admin_email, ignore_error=True)
        if user:
            return user
        data = {}
        data["fullname"] = "Admin"
        data["email"] = settings.default_admin_email
        data["password"] = settings.default_admin_password
        data["is_verified"] = True
        admin = await self.register(data=data)
        return await self.grant_admin(_id=admin["_id"])

    async def register(self, data: schemas.RegisterRequest) -> dict:
        # Set the user role to 'USER' by default.
        data["type"] = value.UserRoles.USER.value
        # Add the current datetime as the creation time.
        data["created_at"] = self.get_current_datetime()
        # Hash the provided password using bcrypt with a generated salt.
        data["password"] = await authentication_services.hash(value=data["password"])
        # Validate the data by creating an instance of the Users model.
        # This process helps validate fields in data according to validation rules defined in the Users model.
        # Then convert it back to a dictionary for saving.
        data_save = models.Users(**data).model_dump(exclude_none=True)
        # Save the user, ensuring the email is unique
        item = await self.save_unique(data=data_save, unique_field="email")

        # Update created_by after register to preserve query ownership logic
        data_update = {"created_by": item["_id"]}
        item = await self.update_by_id(_id=item["_id"], data=data_update)

        # Generate an access token for the user.
        item["access_token"] = await authentication_services.create_access_token(user_id=item["_id"], user_type=item["type"])
        item["token_type"] = "bearer"
        return item

    async def login(self, data: schemas.LoginRequest) -> dict:
        item = await self.get_by_email(email=data["email"], ignore_error=True)
        if not item:
            raise UserErrorCode.Unauthorize()
        # Validate the provided password against the hashed value.
        is_valid_password = await authentication_services.validate_hash(value=data["password"], hashed_value=item["password"])
        if not is_valid_password:
            raise UserErrorCode.Unauthorize()

        # Generate an access token for the user.
        item["access_token"] = await authentication_services.create_access_token(user_id=item["_id"], user_type=item["type"])
        item["token_type"] = "bearer"
        return item

    async def edit(self, _id: str, data: Dict[str, Any], check_modified: bool = True, commons: CommonsDependencies = None) -> dict:
        data["updated_at"] = self.get_current_datetime()
        data["updated_by"] = self.get_current_user(commons=commons)
        return await self.update_by_id(_id=_id, data=data, check_modified=check_modified)

    async def _update_google_id(self, user_id: str, google_id: str):
        data = {}
        data["google_id"] = google_id
        data["is_verified"] = True
        return await self.edit(_id=user_id, data=data, commons=None)

    async def register_with_google(self, fullname: str, email: str, google_id: str, avatar: str) -> dict:
        data = {}
        data["fullname"] = fullname
        data["email"] = email
        data["google_id"] = google_id
        data["avatar"] = avatar
        data["is_verified"] = True
        data["type"] = value.UserRoles.USER.value
        data["created_at"] = self.get_current_datetime()
        data_save = models.Users(**data).model_dump()
        item = await self.save_unique(data=data_save, unique_field="email")
        data_update = {"created_by": item["_id"]}
        item = await self.update_by_id(_id=item["_id"], data=data_update)
        item["access_token"] = await authentication_services.create_access_token(user_id=item["_id"], user_type=item["type"])
        item["token_type"] = "bearer"
        return item
    
    async def login_with_google(self, email: str, google_id: str) -> dict:
        # check if the user already exists
        user = await self.get_by_email(email=email)

        if user.get("google_id") is None:
            user = await self._update_google_id(user_id=user["_id"], google_id=google_id)
        elif user["google_id"] != google_id:
            raise UserErrorCode.Unauthorize()

        # Generate authentication response
        user["access_token"] = await authentication_services.create_access_token(user_id=user["_id"], user_type=user["type"])
        user["token_type"] = "bearer"
        return user

    async def send_verification_email(self, user_id: str, email: str, fullname: str) -> None:
        otp = value.generate_numeric_code(length=settings.otp_length)
        data_update = {}
        data_update["verify_email_otp"] = otp
        data_update["verify_email_otp_expire"] = calculator.add_days_to_datetime(days=settings.verification_token_expire_minutes)
        data_update["verify_email_otp_attempts"] = 0
        await self.update_by_id(_id=user_id, data=data_update)
        # Step 2: Save the token to the database
        await user_mail_services.send_verification_email(recipient=email, fullname=fullname, otp=otp)

    async def send_reset_password_email(self, user_id: str, email: str, fullname: str) -> None:
        otp = value.generate_numeric_code(length=settings.otp_length)
        data_update = {}
        data_update["reset_password_otp"] = otp
        data_update["reset_password_otp_expire"] = calculator.add_days_to_datetime(days=settings.reset_password_otp_expire_minutes)
        data_update["reset_password_attempts"] = 0
        await self.update_by_id(_id=user_id, data=data_update)
        # Step 3: Send the reset password email
        await user_mail_services.send_reset_password_email(recipient=email, fullname=fullname, otp=otp)

    async def increment_reset_password_attempts(self, user_id: str) -> dict:
        user = await self.get_by_id(_id=user_id)
        current_attempts = user.get("reset_password_attempts", 0)
        data_update = {}
        data_update["reset_password_attempts"] = current_attempts + 1
        return await self.update_by_id(_id=user_id, data=data_update)

    async def increment_verify_email_attempts(self, user_id: str) -> dict:
        user = await self.get_by_id(_id=user_id)
        current_attempts = user.get("verify_email_otp_attempts", 0)
        data_update = {}
        data_update["verify_email_otp_attempts"] = current_attempts + 1
        return await self.update_by_id(_id=user_id, data=data_update)
    
    async def update_password(self, user_id: str, password: str) -> dict:
        reset_fields = ["reset_password_otp", "reset_password_otp_expire", "reset_password_attempts"]
        data = {}
        data["password"] = await authentication_services.hash(value=password)
        await self.delete_fields(_id=user_id, field_names=reset_fields)
        return await self.edit(_id=user_id, data=data, check_modified=False, commons=None)
    
    async def verify_email(self, user_id: str) -> dict:
        reset_fields = ["verify_email_otp", "verify_email_otp_expire", "verify_email_otp_attempts"]
        data_update = {}
        data_update["is_verified"] = True
        await self.delete_fields(_id=user_id, field_names=reset_fields)
        return await self.edit(_id=user_id, data=data_update)

user_crud = BaseCRUD(database_engine=app_engine, collection="users")
user_services = UserServices(service_name="users", crud=user_crud)
