from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str
    project_path: str = Field(default="/opt/projects/app")
    logs_path: str = Field(default="/opt/projects/app/logs/access.log")
    cors_origin: list = Field(default=["http://localhost", "http://localhost:3000", "https://eventorize.kiet.site"])

    def is_production(self) -> bool:
        return self.environment == "dev"

settings = Settings()
