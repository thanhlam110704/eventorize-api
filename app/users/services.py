from io import BytesIO
from typing import Any, Dict

import xlsxwriter
from auth.services import authentication_services
from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine
from fastapi import BackgroundTasks, Response
from partners.v1.resend.services import user_mail_services
from utils import calculator, converter, value

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
        if not item.get("password"):
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

    async def get_total_users(self, start_date, end_date) -> int:
        return await self.get_all(query={"is_verified": True, "created_at": {"$gte": start_date, "$lte": end_date}})

    async def export_users(self, data) -> dict:
        date = self.get_current_datetime()
        date_str = converter.convert_datetime_to_str(date)
        filename = f"{date_str}-ReportUsers.xlsx"

        buffer = BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet("Users")

        # Define styles
        header_format = workbook.add_format({"bold": True, "bg_color": "#4F81BD", "color": "white", "align": "center", "valign": "vcenter", "border": 1})

        cell_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1})

        date_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1, "num_format": "yyyy-mm-dd hh:mm:ss"})

        # Define necessary fields
        fields = ["fullname", "email", "type", "is_verified", "phone", "company", "position", "city", "created_at"]

        # Write headers
        for col, field in enumerate(fields):
            worksheet.write(0, col, field.replace("_", " ").title(), header_format)
            worksheet.set_column(col, col, 20)  # Set column width

        # Write data
        for row, user in enumerate(data, start=1):
            for col, field in enumerate(fields):
                value = user.get(field, "")

                # Handle datetime objects
                if field == "created_at" and value:
                    worksheet.write(row, col, value, date_format)
                # Handle boolean values
                elif field == "is_verified":
                    worksheet.write(row, col, "Yes" if value else "No", cell_format)
                # Handle other values
                else:
                    worksheet.write(row, col, value, cell_format)

        # Add a summary section
        summary_row = len(data) + 3
        worksheet.write(summary_row, 0, "Total Users:", header_format)
        worksheet.write(summary_row, 1, len(data), cell_format)

        worksheet.write(summary_row + 1, 0, "Admin Users:", header_format)
        worksheet.write(summary_row + 1, 1, len([u for u in data if u.get("type") == "admin"]), cell_format)

        worksheet.write(summary_row + 2, 0, "Regular Users:", header_format)
        worksheet.write(summary_row + 2, 1, len([u for u in data if u.get("type") == "user"]), cell_format)

        worksheet.write(summary_row + 3, 0, "Verified Users:", header_format)
        worksheet.write(summary_row + 3, 1, len([u for u in data if u.get("is_verified")]), cell_format)

        # Close workbook and return response
        workbook.close()
        buffer.seek(0)

        return Response(
            buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
            background=BackgroundTasks(buffer.close()),
        )


user_crud = BaseCRUD(database_engine=app_engine, collection="users")
user_services = UserServices(service_name="users", crud=user_crud)
