from core.controllers import BaseControllers, CommonsDependencies
from core.services import BaseServices
from fastapi import Request
from partners.v1.google.services import google_sso_services
from users.controllers import user_controllers

from . import schemas
from .config import settings
from .services import authentication_services


class AuthenticationControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def google_login(self) -> dict:
        """
        Generate and return the Google login redirect URL.
        """
        redirect_url = await google_sso_services.get_login_redirect()
        return {"redirect_url": redirect_url}

    async def google_callback(self, request: Request) -> str:
        """
        Handle the Google SSO callback, process user information, and create a token.
        """
        # Process the callback and get user information
        data = await google_sso_services.verify_and_process(request)
        user = await user_controllers.single_sign_on_with_google(data=data)

        return f"{settings.frontend_url}/auth-callback?access_token={user['access_token']}&token_type={user['token_type']}"

    async def verify_email(self, data: schemas.VerifyEmailRequest) -> dict:
        data = data.model_dump()
        return await user_controllers.verify_email(email=data["email"], otp=data["otp"])

    async def resend_verification_email(self, commons: CommonsDependencies) -> dict:
        await user_controllers.send_verification_email(commons=commons)

    async def forgot_password(self, data: schemas.ForgotPasswordRequest) -> None:
        data = data.model_dump()
        # Fetch user by email
        user = await user_controllers.get_by_email(email=data["email"], ignore_error=True)
        if not user:
            # Avoid leaking user existence info
            return
        # Send reset password email
        await user_controllers.send_reset_password_email(user_id=user["_id"], email=user["email"], fullname=user["fullname"])

    async def reset_password(self, data: schemas.ResetPasswordRequest) -> None:
        data = data.model_dump()
        await user_controllers.verify_reset_password_otp(email=data["email"], otp=data["otp"])
        await user_controllers.reset_password(email=data["email"], password=data["new_password"])


authentication_controllers = AuthenticationControllers(controller_name="authentication", service=authentication_services)
