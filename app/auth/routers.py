from core.schemas import CommonsDependencies
from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from users import schemas as user_schemas
from users.controllers import user_controllers
from . import schemas
from .controllers import authentication_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/auth"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.post("/auth/google/login", status_code=200, responses={200: {"description": "Generate Google login URL"}})
    async def google_login(self):
        """
        Generate and return Google's login page URL.
        """
        return await authentication_controllers.google_login()

    @router.get("/auth/google/callback", status_code=200, responses={200: {"model": user_schemas.LoginResponse, "description": "Handle Google SSO callback"}})
    async def callback(self, request: Request):
        """
        Handle the callback from Google after login and process user information.
        """
        redirect_url = await authentication_controllers.google_callback(request)
        return RedirectResponse(url=redirect_url)
    
    @router.post("/auth/google/android", status_code=200, responses={200: {"model": user_schemas.LoginResponse, "description": "Google SSO for Android"}})
    async def google_sso_android(self, data: user_schemas.GoogleSSORequest):
        """
        Handle Google SSO for Android by processing user data and returning an access token.
        """
        result = await user_controllers.single_sign_on_with_google(data=data)
        return user_schemas.LoginResponse(**result)

    @router.post("/auth/verify-email", status_code=200, responses={200: {"model": user_schemas.Response, "description": "Verify user's email address successfully"}})
    async def verify_email(self, data: schemas.VerifyEmailRequest):
        results = await authentication_controllers.verify_email(data=data)
        return user_schemas.Response(**results)

    @router.post("/auth/resend-verification-email", status_code=200, responses={200: {"description": "Resend the email verification link"}})
    async def resend_verification_email(self):
        await authentication_controllers.resend_verification_email(commons=self.commons)
        return schemas.ResendVerificationEmailResponse()

    @router.post("/auth/forgot-password", status_code=200, responses={200: {"description": "Password reset email sent."}})
    async def forgot_password(self, data: schemas.ForgotPasswordRequest):
        await authentication_controllers.forgot_password(data=data)
        return schemas.ForgotPasswordResponse()

    @router.post("/auth/reset-password", status_code=200, responses={200: {"description": "Reset password success."}})
    async def reset_password(self, data: schemas.ResetPasswordRequest):
        await authentication_controllers.reset_password(data=data)
        return schemas.ResetPasswordResponse()
