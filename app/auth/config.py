from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

PUBLIC_APIS = [
    "/docs",
    "/openapi.json",
    "/redoc",
    "/v1/health/ping",
    "/v1/users/register",
    "/v1/users/login",
    ["/v1/events", "GET"],
    ["/v1/events/{_id}", "GET"],
    ["/v1/home/events/{event_id}/agendas", "GET"],
    ["/v1/home/events/{event_id}/agendas/{agenda_id}", "GET"],
    ["/v1/home/organizers/{_id}", "GET"],
    ["/v1/locations/province", "GET"],
    ["/v1/locations/districts", "GET"],
    ["/v1/locations/wards", "GET"],
    {"/v1/event/{event_id}/tickets/{_id}", "GET"},
    "/v1/home/event/{event_id}/tickets",
    "/v1/auth/google/login",
    "/v1/auth/google/android",
    "/v1/auth/google/callback",
    "/v1/auth/verify-email",
    "/v1/auth/forgot-password",
    "/v1/auth/reset-password",
]


class Settings(BaseSettings):
    access_token_expire_day: int = Field(default=3)
    secret_key: str
    algorithm: str
    frontend_url: Optional[str] = None


settings = Settings()
