from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    log_level: str = "INFO"
    strategy: str = "cheapest_asset_covering_request_volume"
