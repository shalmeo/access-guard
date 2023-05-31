import enum
import uuid
from datetime import datetime

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base


class NotificationType(enum.Enum):
    ACCOUNT_EXPIRED = "ACCOUNT_EXPIRED"
    ACCOUNT_EXPIRED_SOON = "ACCOUNT_EXPIRED_SOON"
    ACCOUNT_LOGINS_LIMIT_EXCEEDED = "ACCOUNT_LOGINS_LIMIT_EXCEEDED"


class Notification(Base):
    __tablename__ = "notifications"

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    notificaion_id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    notifcation_type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, create_constraint=False, native_enum=False),
    )
