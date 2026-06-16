from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_NAME: str = "tuiReader"
    API_BASE_URL: HttpUrl = HttpUrl("https://tl.rulate.ru/api3/")

    API_KEY: str = "fpoiKLUues81werht039"
    API_DEV_LOGIN_KEY: str = """MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2pmm/NGAPoi1yRtJQ6M/HnI1wogATo5jezm0B1NELYmpeCt1DgxBFwmbTBRGh7GBi8HzzPW+m4ZsMxP8WDBmxvEjMHJRyVu5nqbYGd38KRB4A0RYQfBAVj/ENF/IKELjtOcU9wXdwku1Hx7T+8d7xL+ScliVHvFPtTYyPrXluQAYUs9Qe0R/Oj0BHRzUisTb7vqHmLeuMx2j9vSnG5iNxL8XLV3viHf7mGXLHtH3sphq0L1kI5+2a0TwUVh2vtF8Lx/TdHXfOM6gA9lrFGrP51ExQ2RdGrieFf0XWD9KQ3LEp+8+JZUeR41hFmbVLgqa4Ed8c0pt2KZUpN7xC2fKsQIDAQAB"""

    class Config:
        env_file = ".env"


config = Config()
