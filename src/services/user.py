from src.core.interfaces.user_repo import UserRepoInterface
from src.models.user import User
from src.services.keyring import KeyringService


class UserService:
    def __init__(self, repo: UserRepoInterface, keyring: KeyringService) -> None:
        self._repo: UserRepoInterface = repo
        self._keyring: KeyringService = keyring

    async def get_me(self) -> User:
        return await self._repo.get_me()

    async def login(self, login: str, password: str) -> User:
        user = await self._repo.login(login, password)

        if user.token:
            self._keyring.set_token(user.token)

        return user
