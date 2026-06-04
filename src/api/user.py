import base64
from typing import override
import aiohttp

from src.api.base import BaseApiClient
from src.config import config

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from src.core.interfaces.user import UserRepoInterface
from src.models.user import User


class UserApiClient(UserRepoInterface, BaseApiClient):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session: aiohttp.ClientSession = session

    def __encrypt(self, data: str) -> str:
        key_bytes = base64.b64decode(config.API_DEV_LOGIN_KEY)
        public_key = RSA.importKey(key_bytes)
        cipher = PKCS1_v1_5.new(public_key)
        encrypted = cipher.encrypt(data.encode("utf-8"))

        return base64.b64encode(encrypted).decode("utf-8")

    @override
    async def login(self, login: str, password: str) -> User:
        enc_login = self.__encrypt(login)
        enc_pass = self.__encrypt(password)

        form = aiohttp.FormData()
        form.add_field("login", enc_login)
        form.add_field("pass", enc_pass)

        async with self._session.post("auth2", data=form) as response:
            data = await self._validate_response(response)

            return User.model_validate(data.response)

    @override
    async def get_me(self) -> User:
        async with self._session.get("getMe") as response:
            data = await self._validate_response(response)

            return User.model_validate(data.response)
