from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DB(BaseModel):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str


class Settings(BaseSettings):
    DB: DB

    model_config = SettingsConfigDict(env_file="./.env", env_nested_delimiter="__")


settings = Settings()  # type: ignore
