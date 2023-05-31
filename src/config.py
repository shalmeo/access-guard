from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    filename: str = "access.guard.db"

    @property
    def uri(self) -> str:
        return f"sqlite:///{self.filename}"


@dataclass(frozen=True)
class NotificationSenderConfig:
    check_interval: int = 30


@dataclass(frozen=True)
class BotConfig:
    # TODO: rewrite to ENV
    token: str = ""
