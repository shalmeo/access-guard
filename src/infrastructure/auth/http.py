from uuid import UUID

from src.application.auth.interfaces import AuthSessionGateway
from src.application.common.exceptions import NotFound
from src.domain.exceptions import AuthenticationError
from src.domain.user import UserId


class HttpAuthenticatorImpl:
    def __init__(self, auth_session_gateway: AuthSessionGateway) -> None:
        self.auth_session_gateway = auth_session_gateway

    def create_session(self, user_id: UserId) -> UUID:
        session = self.auth_session_gateway.create_session(user_id)
        self.auth_session_gateway.commit()

        return session.session_id

    def validate_session(self, session_id: UUID) -> UserId:
        try:
            session = self.auth_session_gateway.get_session_by_id(session_id)
        except NotFound:
            raise AuthenticationError

        return session.user_id
