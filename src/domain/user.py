from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from src.domain.exceptions import AccessExpiredError

UserId = NewType("UserId", int)


@dataclass
class User:
    user_id: UserId | None
    telegram_id: int | None
    name: str
    password: str
    expired_in: datetime

    @classmethod
    def create(
        cls,
        name: str,
        password: str,
        telegram_id: int | None,
        expired_in: datetime,
    ):
        return User(
            user_id=None,
            name=name,
            password=password,
            telegram_id=telegram_id,
            expired_in=expired_in,
        )

    def update(self, name: str | None, telegram_id: int | None) -> None:
        if self._is_expired():
            raise AccessExpiredError

        if name:
            self.name = name

        if telegram_id:
            self.telegram_id = telegram_id

    def set_telegram_id(self, telegram_id: int) -> None:
        if self._is_expired():
            raise AccessExpiredError

        self.telegram_id = telegram_id

    def is_expired(self) -> bool:
        return self._is_expired()

    def _is_expired(self) -> bool:
        return datetime.now() > self.expired_in
