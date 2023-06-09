from typing import Protocol

from src.application.common.interfaces import Commiter
from src.application.user.dto import UserDTO
from src.domain.user import User, UserId


class UserGateway(Commiter, Protocol):
    def get_user_by_id(self, user_id: UserId) -> UserDTO:
        pass

    def get_user_password_by_name(self, name: str) -> str:
        pass

    def get_users(self) -> list[UserDTO]:
        pass

    def acquire_user_by_id(self, user_id: UserId) -> User:
        pass

    def acquire_user_by_name(self, name: str) -> User:
        pass

    def save_user(self, user: User, password: str | None = None) -> None:
        pass
