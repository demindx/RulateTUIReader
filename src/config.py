from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_NAME: str = "tuiReader"
    API_BASE_URL: HttpUrl = HttpUrl("https://tl.rulate.ru/api3/")
    API_KEY: str
    API_DEV_LOGIN_KEY: str
    TEST_LOGIN: str
    TEST_PASS: str

    class Config:
        env_file = ".env"


config = Config()
