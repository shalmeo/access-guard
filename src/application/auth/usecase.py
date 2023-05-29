from src.application.auth.dto import LoginResultDTO
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
        user_password = self.db_gateway.get_user_password_by_name(data.name)

        if not verificate_password(password=data.password, expected_password=user_password):
            raise AuthenticationError

        if user.is_expired():
            raise AccessExpiredError

        return user.user_id
