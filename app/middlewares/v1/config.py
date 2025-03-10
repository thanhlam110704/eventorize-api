from pydantic_settings import BaseSettings

ACTION_EXCEPT = ["/v1/ping", "/docs", "/openapi.json", "/favicon.ico"]

# Don't send notification to errors channel
UNSEND_NOTIFY_ENDPOINTS = ["/v1/users/me"]


class Settings(BaseSettings):
    environment: str


settings = Settings()
