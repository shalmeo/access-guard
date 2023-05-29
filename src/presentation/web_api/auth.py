from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.user import UserId


class HttpAuthenticator(ABC):
    @abstractmethod
    def create_session(self, user_id: UserId) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def validate_session(self, session_id: UUID) -> UserId:
        raise NotImplementedError
