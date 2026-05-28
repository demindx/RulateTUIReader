import base64
import aiohttp

from src.config import config
from src.core.exceptions import RequestException
from src.types.response import RulateResponse
from src.types.user import User

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from src.core import keyring


class UserApiClient:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.__session: aiohttp.ClientSession = session

    async def login(self, login: str, password: str) -> User:
        enc_login = self.__encrypt(login)
        enc_pass = self.__encrypt(password)

        form = aiohttp.FormData()
        form.add_field("login", enc_login)
        form.add_field("pass", enc_pass)

        async with self.__session.post("auth2", data=form) as resp:
            data = RulateResponse.model_validate(await resp.json())

            if data.status == "fail":
                raise RequestException(data.msg)

            user = User.model_validate(data.response)

            if user.token:
                keyring.set_token(user.token)

            return user

    async def get_me(self) -> User:

        async with self.__session.get("getMe") as response:
            data = RulateResponse.model_validate(await response.json())

            if data.status == "fail":
                raise RequestException(data.msg)

            return User.model_validate(data.response)

    def __encrypt(self, data: str) -> str:
        key_bytes = base64.b64decode(config.API_DEV_LOGIN_KEY)
        public_key = RSA.importKey(key_bytes)
        cipher = PKCS1_v1_5.new(public_key)
        encrypted = cipher.encrypt(data.encode("utf-8"))

        return base64.b64encode(encrypted).decode("utf-8")
