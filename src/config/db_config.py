import os

from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	postgres_url: PostgresDsn = Field(env='postgres_url')

	model_config = SettingsConfigDict(
		env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
		env_file_encoding="utf-8",
	)