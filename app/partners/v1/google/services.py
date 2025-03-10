from fastapi_sso.sso.google import GoogleSSO

from .config import settings


class GoogleSSOService:
    def __init__(self, client_id, client_secret, redirect_uri) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.google_sso = GoogleSSO(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri)

    async def get_login_redirect(self):
        """
        Generate the Google SSO login redirect URL.
        """
        return await self.google_sso.get_login_url()

    async def verify_and_process(self, request):
        """
        Process the Google SSO callback and retrieve user information.
        """
        return await self.google_sso.verify_and_process(request)


google_sso_services = GoogleSSOService(client_id=settings.client_id_google, client_secret=settings.client_secret_google, redirect_uri=settings.redirect_uri_google)
