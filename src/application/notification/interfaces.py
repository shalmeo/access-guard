from typing import Protocol

from src.application.common.interfaces import Commiter


class NotificationGateway(Commiter, Protocol):
    pass
