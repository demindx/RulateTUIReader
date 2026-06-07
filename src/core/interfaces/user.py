from abc import ABC, abstractmethod

from src.models.bookmark import BookmarkModel
from src.models.user import UserModel


class UserRepoInterface(ABC):
    @abstractmethod
    async def login(self, login: str, password: str) -> UserModel: ...

    @abstractmethod
    async def get_me(self) -> UserModel: ...

    @abstractmethod
    async def get_bookmarks(self) -> list[BookmarkModel]: ...
