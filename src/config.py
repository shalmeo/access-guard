from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    filename: str = "access.guard.db"

    @property
    def uri(self) -> str:
        return f"sqlite:///{self.filename}"
