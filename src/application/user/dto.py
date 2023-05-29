from dataclasses import dataclass
from datetime import datetime

from src.domain.user import UserId


@dataclass(frozen=True)
class UserDTO:
    name: str
    expired_in: datetime

    @property
    def expired(self) -> bool:
        return self.expired_in < datetime.now()


@dataclass(frozen=True)
class CreateUserDTO:
    name: str
    password: str
    expired_in: datetime


@dataclass(frozen=True)
class UpdateUserDTO:
    user_id: UserId
    name: str | None
    expired_in: datetime | None
