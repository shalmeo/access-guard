from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.user import UserId


@dataclass(frozen=True)
class LoginResultDTO:
    name: str
    password: str


@dataclass(frozen=True)
class SessionDTO:
    session_id: UUID
    user_id: UserId
