from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    database_url: str = Field(validation_alias="DATABASE_URL")
    env: str = Field(validation_alias="ENV")
    frontend_url: str = Field(validation_alias="FRONTEND_URL")
    debug: bool = Field(validation_alias="DEBUG")


config = Config()
