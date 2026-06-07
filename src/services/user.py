from src.core.interfaces.user import UserRepoInterface
from src.models.bookmark import BookmarkModel
from src.models.user import UserModel
from src.services.keyring import KeyringService


class UserService:
    def __init__(self, repo: UserRepoInterface, keyring: KeyringService) -> None:
        self._repo: UserRepoInterface = repo
        self._keyring: KeyringService = keyring
        self._user: UserModel | None = None

    async def get_me(self) -> UserModel:
        if self._user is None:
            self._user = await self._repo.get_me()

        return self._user

    async def login(self, login: str, password: str) -> UserModel:
        user = await self._repo.login(login, password)

        if user.token:
            self._keyring.set_token(user.token)

        return user

    async def get_bookmarks(self) -> list[BookmarkModel]:
        # if self._user and self._user.token:
        return await self._repo.get_bookmarks()
