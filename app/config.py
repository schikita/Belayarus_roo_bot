from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    bot_token: str = Field(..., alias="BOT_TOKEN")
    database_url: str = Field(..., alias="DATABASE_URL")
    redis_url: Optional[str] = Field(None, alias="REDIS_URL")
    daily_broadcast_time: str = Field(..., alias="DAILY_BROADCAST_TIME")
    bot_admins: Optional[List[int]] = Field(default_factory=list, alias="BOT_ADMINS")


settings = Settings()
