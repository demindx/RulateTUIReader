import aiohttp

from src.api.book import BookApiClient
from src.api.user import UserApiClient
from src.services.book import BookService
from src.services.image import ImageService
from src.services.keyring import KeyringService
from src.services.user import UserService


class AppService:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.keyring: KeyringService = KeyringService()
        self.user: UserService = UserService(UserApiClient(session), self.keyring)
        self.book: BookService = BookService(BookApiClient(session))
        self.image: ImageService = ImageService(session)
