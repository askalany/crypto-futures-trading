from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env", env_file_encoding="utf-8", extra="allow"
    )
    KEY: str = Field(default="", alias="KEY")
    SECRET: str = Field(default="", alias="SECRET")
    BASE_URL: str = Field(default="", alias="BASE_URL")
    STREAM_URL: str = Field(default="", alias="STREAM_URL")
