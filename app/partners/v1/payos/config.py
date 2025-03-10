from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    client_id_payos: str
    api_key_payos: str
    checksum_key_payos: str
    cancel_url_payos: str
    return_url_payos: str


settings = Settings()
