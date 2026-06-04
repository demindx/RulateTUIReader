from abc import ABC, abstractmethod

from src.models.user import User


class UserRepoInterface(ABC):
    @abstractmethod
    async def login(self, login: str, password: str) -> User: ...

    @abstractmethod
    async def get_me(self) -> User: ...
