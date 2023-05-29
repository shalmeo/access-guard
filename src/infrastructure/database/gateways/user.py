from sqlalchemy import select

from src.application.common.exceptions import NotFound
from src.application.user.dto import UserDTO
from src.application.user.interfaces import UserGateway
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

        return UserDTO(name=db_user.name, expired_in=db_user.expired_in)

    def get_user_password_by_name(self, name: str) -> str:
        db_user: database.User = self.session.scalar(
            select(database.User).where(database.User.name == name),
        )

        if db_user is None:
            raise NotFound

        return db_user.password

    def get_users(self) -> list[UserDTO]:
        db_users = self.session.scalars(select(database.User))
        return [UserDTO(name=db_user.name, expired_in=db_user.expired_in) for db_user in db_users]

    def acquire_user_by_id(self, user_id: UserId) -> User:
        db_user: database.User = self.session.scalar(
            select(database.User).where(database.User.user_id == user_id),
        )

        if db_user is None:
            raise NotFound

        return User(
            user_id=db_user.user_id,
            name=db_user.name,
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
            name=db_user.name,
            expired_in=db_user.expired_in,
        )

    def save_user(self, user: User, password: str | None = None) -> None:
        db_user = self._user(user.user_id)

        if db_user is None:
            db_user = database.User(name=user.name, password=password, expired_in=user.expired_in)
        else:
            db_user.name = user.name
            db_user.expired_in = user.expired_in
            if not (password is None):
                db_user.password = password

        self.session.merge(db_user)
        user.user_id = db_user.user_id
