from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DB(BaseModel):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    @computed_field
    def URL(self) -> str:
        return f"mysql+aiomysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class APP(BaseModel):
    PORT: int
    FRONTEND_URL: str


class Settings(BaseSettings):
    DB: DB
    APP: APP

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()  # type: ignore
