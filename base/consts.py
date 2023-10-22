from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from data.enums import TickerSymbol
from utils.fileutils import get_inputs_from_file
from base.models.FileInput import FileInput


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env", env_file_encoding="utf-8", extra="allow")
    KEY: str = Field(default="", alias="KEY")
    SECRET: str = Field(default="", alias="SECRET")
    BASE_URL: str = Field(default="", alias="BASE_URL")
    STREAM_URL: str = Field(default="", alias="STREAM_URL")
    file_input: FileInput = Field(default_factory=lambda: get_inputs_from_file())
