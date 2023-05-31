from src.application.auth.dto import LoginResultDTO, TelegramLoginResultDTO
from src.application.common.usecase import UseCase
from src.application.user.interfaces import UserGateway
from src.domain.exceptions import AccessExpiredError, AuthenticationError
from src.domain.user import UserId
from src.infrastructure.auth.password import verificate_password


class Authenticate(UseCase[LoginResultDTO, UserId]):
    def __init__(
        self,
        db_gateway: UserGateway,
    ):
        self.db_gateway = db_gateway

    def __call__(self, data: LoginResultDTO) -> UserId:
        user = self.db_gateway.acquire_user_by_name(data.name)

        if not verificate_password(password=data.password, expected_password=user.password):
            raise AuthenticationError

        if user.is_expired():
            raise AccessExpiredError

        return user.user_id


class AuthenticateTelegram(UseCase[TelegramLoginResultDTO, None]):
    def __init__(
        self,
        db_gateway: UserGateway,
    ):
        self.db_gateway = db_gateway

    def __call__(self, data: TelegramLoginResultDTO) -> None:
        user = self.db_gateway.acquire_user_by_id(data.user_id)

        user.set_telegram_id(data.telegram_id)
        self.db_gateway.save_user(user)
        self.db_gateway.commit()

        return user.user_id
