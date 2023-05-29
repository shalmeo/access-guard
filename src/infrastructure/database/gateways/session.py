from uuid import UUID

from sqlalchemy import select

from src.application.auth.dto import SessionDTO
from src.application.auth.interfaces import AuthSessionGateway
from src.application.common.exceptions import NotFound
from src.domain.user import UserId
from src.infrastructure import database
from src.infrastructure.database.gateways.common import CommiterImpl


class AuthSessionGatewayImpl(AuthSessionGateway, CommiterImpl):
    def get_session_by_id(self, session_id: UUID) -> SessionDTO:
        db_session = self.session.scalar(
            select(database.Session).where(database.Session.session_id == str(session_id)),
        )

        if db_session is None:
            raise NotFound

        return SessionDTO(
            session_id=UUID(db_session.session_id),
            user_id=db_session.user_id,
        )

    def create_session(self, user_id: UserId) -> SessionDTO:
        db_session = database.Session(user_id=user_id)
        self.session.add(db_session)
        self.session.flush((db_session,))
        return SessionDTO(
            session_id=UUID(db_session.session_id),
            user_id=db_session.user_id,
        )
