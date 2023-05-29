from src.application.common.usecase import UseCase
from src.application.user.dto import CreateUserDTO, UpdateUserDTO, UserDTO
from src.application.user.interfaces import UserGateway
from src.domain.exceptions import AuthenticationError
from src.domain.user import User, UserId


class GetUserById(UseCase[UserId, UserDTO]):
    def __init__(self, db_gateway: UserGateway) -> None:
        self.db_gateway = db_gateway

    def __call__(self, data: UserId) -> UserDTO:
        user = self.db_gateway.acquire_user_by_id(data)
        if user.is_expired():
            raise AuthenticationError

        return UserDTO(name=user.name, expired_in=user.expired_in)


class GetUsers(UseCase[None, list[UserDTO]]):
    def __init__(self, db_gateway: UserGateway) -> None:
        self.db_gateway = db_gateway

    def __call__(self, data: object) -> list[UserDTO]:
        return self.db_gateway.get_users()


class CreateUser(UseCase[CreateUserDTO, UserId]):
    def __init__(self, db_gateway: UserGateway) -> None:
        self.db_gateway = db_gateway

    def __call__(self, data: CreateUserDTO) -> UserId:
        user = User.create(name=data.name, expired_in=data.expired_in)
        self.db_gateway.save_user(user, password=data.password)
        self.db_gateway.commit()
        return user.user_id


class UpdateUser(UseCase[UpdateUserDTO, UserId]):
    def __init__(self, db_gateway: UserGateway) -> None:
        self.db_gateway = db_gateway

    def __call__(self, data: UpdateUserDTO) -> UserId:
        user = self.db_gateway.acquire_user_by_id(data.user_id)
        if user.is_expired():
            raise AuthenticationError

        user.update(name=data.name, expired_in=data.expired_in)
        self.db_gateway.save_user(user)
        self.db_gateway.commit()

        return user.user_id
