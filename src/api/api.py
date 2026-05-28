import aiohttp

from src.api.book import BookApiClient
from src.api.user import UserApiClient


class ApiClient:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.user: UserApiClient = UserApiClient(session)
        self.book: BookApiClient = BookApiClient(session)
