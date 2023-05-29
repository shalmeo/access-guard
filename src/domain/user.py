from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from src.domain.exceptions import AccessExpiredError

UserId = NewType("UserId", int)


@dataclass
class User:
    user_id: UserId | None
    name: str
    expired_in: datetime

    @classmethod
    def create(cls, name: str, expired_in: datetime):
        return User(user_id=None, name=name, expired_in=expired_in)

    def update(self, name: str | None, expired_in: datetime | None) -> None:
        if self._is_expired():
            raise AccessExpiredError

        if not (name is None):
            self.name = name

        if not (expired_in is None):
            self.expired_in = expired_in

    def is_expired(self) -> bool:
        return self._is_expired()

    def _is_expired(self) -> bool:
        return self.expired_in < datetime.now()
