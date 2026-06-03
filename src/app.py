import aiohttp
from src.core.exceptions import RequestException
from src.services.app import AppService
from src.services.keyring import KeyringService
from src.ui.ui import UI
from src.config import config


async def _api_key_middleware(
    req: aiohttp.ClientRequest, handler: aiohttp.ClientHandlerType
) -> aiohttp.ClientResponse:

    req.url = req.url.update_query({"key": config.API_KEY})

    return await handler(req)


async def _auth_middleware(
    req: aiohttp.ClientRequest, handler: aiohttp.ClientHandlerType
) -> aiohttp.ClientResponse:
    keyring = KeyringService()

    token = keyring.get_token()

    if not token:
        raise RequestException("You must login")

    req.headers["Authorization"] = f"Bearer {token}"

    return await handler(req)


class App:
    def __init__(self) -> None:
        self.client: AppService | None = None
        self.ui: UI = UI()

    async def start(self) -> None:
        async with aiohttp.ClientSession(
            base_url=str(config.API_BASE_URL),
            headers={"user-agent": "RuLateApp Android"},
            middlewares=(_api_key_middleware, _auth_middleware),
        ) as session:
            self.client = AppService(session)

            user = await self.client.user.login(config.TEST_LOGIN, config.TEST_PASS)

            print(user)

            new_user = await self.client.user.get_me()

            print(new_user)

            # await self.ui.run_async()
