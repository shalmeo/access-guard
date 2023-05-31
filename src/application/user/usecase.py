from datetime import datetime, timedelta

from telebot import TeleBot

from src.application.common.usecase import UseCase
from src.application.user.dto import CreateUserDTO, SessionDTO, UpdateUserDTO, UserDTO
from src.application.user.interfaces import SessionGateway, UserGateway
from src.domain.exceptions import AuthenticationError
from src.domain.user import User, UserId

MAX_LOGINS_COUNT = 3


class GetUserById(UseCase[UserId, UserDTO]):
    def __init__(self, db_gateway: UserGateway) -> None:
        self.db_gateway = db_gateway

    def __call__(self, data: UserId) -> UserDTO:
        user = self.db_gateway.acquire_user_by_id(data)
        if user.is_expired():
            raise AuthenticationError

        return UserDTO(user_id=user.user_id, name=user.name, telegram_id=user.telegram_id, expired_in=user.expired_in)


class GetUsers(UseCase[None, list[UserDTO]]):
    def __init__(self, db_gateway: UserGateway) -> None:
        self.db_gateway = db_gateway

    def __call__(self, data: object) -> list[UserDTO]:
        return self.db_gateway.get_users()


class CreateUser(UseCase[CreateUserDTO, UserId]):
    def __init__(self, db_gateway: UserGateway) -> None:
        self.db_gateway = db_gateway

    def __call__(self, data: CreateUserDTO) -> UserId:
        user = User.create(
            name=data.name,
            password=data.password,
            telegram_id=None,
            expired_in=data.expired_in,
        )
        self.db_gateway.save_user(user)
        self.db_gateway.commit()
        return user.user_id


class UpdateUser(UseCase[UpdateUserDTO, UserId]):
    def __init__(self, db_gateway: UserGateway) -> None:
        self.db_gateway = db_gateway

    def __call__(self, data: UpdateUserDTO) -> UserId:
        user = self.db_gateway.acquire_user_by_id(data.user_id)
        if user.is_expired():
            raise AuthenticationError

        user.update(name=data.name, telegram_id=None)
        self.db_gateway.save_user(user)
        self.db_gateway.commit()

        return user.user_id


class SendNotifications(UseCase[..., ...]):
    def __init__(self, user_gateway: UserGateway, session_gateway: SessionGateway, bot: TeleBot) -> None:
        self.user_gateway = user_gateway
        self.session_gateway = session_gateway
        self.bot = bot

    def __call__(self, data: object) -> None:
        sent_messages = 0

        text_expired = "Срок действия вашего аккаунта истек! <code>{expired_in}</code>"
        text_expired_soon = "Срок действия вашего аккаунта скоро истекает! <code>{expired_in}</code>"
        text_logins_limit_exceeded = "Превышен лимит входа в аккаунт!"

        users = self.user_gateway.get_users()
        for user in users:
            if not user.telegram_id:
                continue

            if user.expired:
                self.bot.send_message(
                    chat_id=user.telegram_id,
                    text=text_expired.format(expired_in=user.expired_in.strftime("%d.%m.%Y %H:%M")),
                )
                sent_messages += 1
            elif user.expired_in - datetime.now() < timedelta(days=30):
                self.bot.send_message(
                    chat_id=user.telegram_id,
                    text=text_expired_soon.format(expired_in=user.expired_in.strftime("%d.%m.%Y %H:%M")),
                )
                sent_messages += 1

            sessions = self.session_gateway.get_sessions_by_user_id(user_id=user.user_id, limit=5)

            logins_count = 0
            prev_session: SessionDTO | None = None
            for session in sessions:
                if not isinstance(prev_session, SessionDTO):
                    prev_session = session
                    continue

                if session.created_at - prev_session.created_at < timedelta(minutes=10):
                    logins_count += 1

                if logins_count >= MAX_LOGINS_COUNT:
                    break

                prev_session = session

            if logins_count >= MAX_LOGINS_COUNT:
                self.bot.send_message(chat_id=user.telegram_id, text=text_logins_limit_exceeded)
                sent_messages += 1

        print(f"{datetime.now()} Sent messages: {sent_messages}")
