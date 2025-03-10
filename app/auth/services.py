from datetime import datetime
from bcrypt import checkpw, gensalt, hashpw
from core.services import BaseServices
from db.base import BaseCRUD
from fastapi import Request
from jose import jwt
from utils import calculator, converter

from .config import PUBLIC_APIS, settings


class AuthenticationServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create_access_token(self, user_id: str, user_type: str) -> dict:
        """
        Creates a JWT access token for the specified user.

        Args:
            user_id (str): The ID of the user for whom the token is being created.
            user_type (str): The type of the user (e.g., admin, customer).

        Returns:
            str: The encoded JWT access token.
        """
        expire = calculator.add_days_to_datetime(days=settings.access_token_expire_day)
        expire_str = converter.convert_datetime_to_str(datetime_obj=expire)
        to_encode = {"user_id": user_id, "user_type": user_type, "expire": expire_str}
        encoded_jwt = jwt.encode(claims=to_encode, key=settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    async def validate_access_token(self, token: str) -> bool:
        """
        Validates a JWT access token.

        Args:
            token (str): The JWT access token to be validated.

        Returns:
            bool: True if the token is valid and not expired, False otherwise.

        """
        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            datetime_obj = converter.convert_str_to_datetime(datetime_str=payload["expire"])
            if datetime.now() > datetime_obj:
                return False
            if not payload.get("user_id"):
                return False
            return payload
        except Exception:
            return False

    def is_path_matching_pattern(self, public_api: str, api_path: str) -> bool:
        """
        Checks if the given API path matches the public API pattern by splitting and comparing segments.

        Args:
            public_api (str): The public API pattern, which may include dynamic segments enclosed in {}.
            api_path (str): The actual API path being accessed.

        Returns:
            bool: True if the API path matches the public API pattern, False otherwise.
        """
        public_api_segments = public_api.strip("/").split("/")
        api_path_segments = api_path.strip("/").split("/")

        if len(public_api_segments) != len(api_path_segments):
            return False

        for public_api_segment, api_path_segment in zip(public_api_segments, api_path_segments):
            if public_api_segment.startswith("{") and public_api_segment.endswith("}"):
                continue
            if public_api_segment != api_path_segment:
                return False
        return True

    async def check_public_api(self, request: Request) -> bool:
        """
        Checks if the API being accessed is a public API.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            bool: True if the API path is listed as a public API, False otherwise.

        """
        api_path = request.url.path
        api_method = request.method
        for public_api in PUBLIC_APIS:
            if isinstance(public_api, str) and self.is_path_matching_pattern(public_api, api_path):
                return True
            if isinstance(public_api, list) and self.is_path_matching_pattern(public_api[0], api_path) and public_api[1] == api_method:
                return True
        return False

    async def hash(self, value) -> bytes:
            """
            Hashes a given string using bcrypt.

            Args:
                value (str): The string to be hashed.

            Returns:
                bytes: The hashed representation of the input string.
            """
            return hashpw(value.encode("utf8"), gensalt())

    async def validate_hash(self, value, hashed_value) -> bool:
        """
        Validates a given string against a hashed value using bcrypt.

        Args:
            value (str): The string to validate.
            hashed_value (bytes): The hashed value to compare against.

        Returns:
            bool: True if the string matches the hash, False otherwise.
        """
        if not checkpw(value.encode("utf-8"), hashed_value):
            return False
        return True

authentication_services = AuthenticationServices(service_name="authentication")
