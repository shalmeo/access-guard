from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import ContextManager

from src.application.auth.usecase import Authenticate
from src.application.user.interfaces import UserGateway
from src.application.user.usecase import GetUserById, UpdateUser


class InteractorFactory(ABC):
    @abstractmethod
    def authenticate(self) -> ContextManager[Authenticate]:
        raise NotImplementedError

    def get_user_by_id(self) -> ContextManager[GetUserById]:
        raise NotImplementedError

    def update_user(self) -> ContextManager[UpdateUser]:
        raise NotImplementedError


class IoC:
    def __init__(self, user_db_gateway: UserGateway) -> None:
        self.user_db_gateway = user_db_gateway

    @contextmanager
    def authenticate(self) -> Authenticate:
        yield Authenticate(db_gateway=self.user_db_gateway)

    @contextmanager
    def get_user_by_id(self) -> GetUserById:
        yield GetUserById(db_gateway=self.user_db_gateway)

    @contextmanager
    def update_user(self) -> UpdateUser:
        yield UpdateUser(db_gateway=self.user_db_gateway)
