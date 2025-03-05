from fastapi_sso.sso.github import GithubSSO

from .config import settings


class GithubServices:
    def __init__(self, github_client_id, github_client_secret, github_redirect_uri) -> None:
        self.github_client_id = github_client_id
        self.github_client_secret = github_client_secret
        self.github_redirect_uri = github_redirect_uri
        self.github_sso = GithubSSO(client_id=self.github_client_id, client_secret=self.github_client_secret, redirect_uri=self.github_redirect_uri)

    async def get_login_redirect(self):
        """
        Generate the Github SSO login redirect URL.
        """
        return await self.github_sso.get_login_url()

    async def verify_and_process(self, request):
        """
        Process the Github SSO callback and retrieve user information.
        """
        return await self.github_sso.verify_and_process(request)


github_services = GithubServices(github_client_id=settings.github_client_id, github_client_secret=settings.github_client_secret, github_redirect_uri=settings.github_redirect_uri)
