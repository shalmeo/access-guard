from sqlalchemy import ScalarResult, select

from src.application.common.exceptions import NotFound
from src.application.user.dto import SessionDTO, UserDTO
from src.application.user.interfaces import SessionGateway, UserGateway
from src.domain.user import User, UserId
from src.infrastructure import database
from src.infrastructure.database.gateways.common import CommiterImpl


class FakeUserGateway(UserGateway):
    def commit(self):
        pass

    def save_user(self, user: User) -> None:
        user.user_id = UserId(0)


class UserGatewayImpl(UserGateway, CommiterImpl):
    def _user(self, user_id: UserId) -> database.User:
        return self.session.scalar(select(database.User).where(database.User.user_id == user_id))

    def get_user_by_id(self, user_id: UserId) -> UserDTO:
        db_user: database.User = self.session.scalar(
            select(database.User).where(database.User.user_id == user_id),
        )

        if db_user is None:
            raise NotFound

        return UserDTO(
            user_id=db_user.user_id, name=db_user.name, telegram_id=db_user.telegram_id, expired_in=db_user.expired_in
        )

    def get_user_password_by_name(self, name: str) -> str:
        db_user: database.User = self.session.scalar(
            select(database.User).where(database.User.name == name),
        )

        if db_user is None:
            raise NotFound

        return db_user.password

    def get_users(self) -> list[UserDTO]:
        db_users = self.session.scalars(select(database.User))
        return [
            UserDTO(
                user_id=db_user.user_id,
                name=db_user.name,
                telegram_id=db_user.telegram_id,
                expired_in=db_user.expired_in,
            )
            for db_user in db_users
        ]

    def acquire_user_by_id(self, user_id: UserId) -> User:
        db_user: database.User = self.session.scalar(
            select(database.User).where(database.User.user_id == user_id),
        )

        if db_user is None:
            raise NotFound

        return User(
            user_id=db_user.user_id,
            telegram_id=db_user.telegram_id,
            name=db_user.name,
            password=db_user.password,
            expired_in=db_user.expired_in,
        )

    def acquire_user_by_name(self, name: str) -> User:
        db_user: database.User = self.session.scalar(
            select(database.User).where(database.User.name == name),
        )

        if db_user is None:
            raise NotFound

        return User(
            user_id=db_user.user_id,
            telegram_id=db_user.telegram_id,
            name=db_user.name,
            password=db_user.password,
            expired_in=db_user.expired_in,
        )

    def save_user(self, user: User) -> None:
        db_user = database.User(
            user_id=user.user_id,
            telegram_id=user.telegram_id,
            name=user.name,
            password=user.password,
            expired_in=user.expired_in,
        )

        self.session.merge(db_user)
        user.user_id = db_user.user_id


class SessionGatewayImpl(SessionGateway, CommiterImpl):
    def get_sessions_by_user_id(
        self, user_id: UserId, offset: int | None = None, limit: int | None = None
    ) -> list[SessionDTO]:
        stmt = (
            select(database.Session)
            .where(database.Session.user_id == user_id)
            .order_by(database.Session.created_at.desc())
        )

        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        sessions: ScalarResult[database.Session] = self.session.scalars(stmt)

        return [
            SessionDTO(
                created_at=session.created_at,
                session_id=session.session_id,
                user_id=session.user_id,
            )
            for session in sessions
        ]
