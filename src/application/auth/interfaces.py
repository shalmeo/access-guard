from typing import Protocol
from uuid import UUID

from src.application.auth.dto import SessionDTO
from src.application.common.interfaces import Commiter
from src.domain.user import UserId


class AuthSessionGateway(Commiter, Protocol):
    def get_session_by_id(self, session_id: UUID) -> SessionDTO:
        pass

    def create_session(self, user_id: UserId) -> SessionDTO:
        pass
