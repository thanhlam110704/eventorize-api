from auth.services import authentication_services
from starlette.middleware.base import BaseHTTPMiddleware

from .exceptions import ErrorCode as MiddlewareErrorCode

# from users.services import user_services


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        # Check if the API being accessed is a public API
        is_public_api = await authentication_services.check_public_api(request=request)
        if is_public_api:
            request.state.payload = {"is_public_api": True}
        else:
            token = request.headers.get("Authorization")
            if not token:
                return MiddlewareErrorCode.Unauthorize()
            payload = await authentication_services.validate_access_token(token=token)
            if not payload:
                return MiddlewareErrorCode.Unauthorize()
            # user = await user_services.get_by_id(_id=payload["user_id"], ignore_error=True)
            # if user is None:
            #     return MiddlewareErrorCode.Unauthorize()
            # is_verified = user.get("is_verified", False)
            # if not is_verified and request.url.path != "/v1/auth/resend-verification-email":
            #     return MiddlewareErrorCode.EmailNotVerified()
            request.state.payload = payload

        response = await call_next(request)
        return response
