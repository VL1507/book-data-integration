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
        return f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class Settings(BaseSettings):
    DB: DB

    model_config = SettingsConfigDict(
        env_nested_delimiter="_",
        extra="ignore",
    )


settings = Settings()  # type: ignore
