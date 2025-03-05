from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    error_bot_token_telegram: Optional[str] = None
    bot_token_telegram: Optional[str] = None
    error_channel_ids: str = "-4636295777"
    order_channel_ids: str = "-4664082397"


settings = Settings()
