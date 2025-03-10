from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    total_request_timeout: float = Field(default=60.0)  # Timeout for the entire request
    server_connection_timeout: float = Field(default=10.0)  # Timeout for establishing a connection
    max_retry_attempts: int = Field(default=3)  # Maximum number of retry attempts for failed requests


settings = Settings()