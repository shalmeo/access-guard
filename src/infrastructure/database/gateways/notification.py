from src.application.notification.interfaces import NotificationGateway
from src.infrastructure.database.gateways.common import CommiterImpl


class NotificationGatewayImpl(NotificationGateway, CommiterImpl):
    pass
