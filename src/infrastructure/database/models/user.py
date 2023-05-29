from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    expired_in: Mapped[datetime] = mapped_column(nullable=False)
