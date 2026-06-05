from src.core.interfaces.user import UserRepoInterface
from src.models.user import UserModel
from src.services.keyring import KeyringService


class UserService:
    def __init__(self, repo: UserRepoInterface, keyring: KeyringService) -> None:
        self._repo: UserRepoInterface = repo
        self._keyring: KeyringService = keyring

    async def get_me(self) -> UserModel:
        return await self._repo.get_me()

    async def login(self, login: str, password: str) -> UserModel:
        user = await self._repo.login(login, password)

        if user.token:
            self._keyring.set_token(user.token)

        return user
