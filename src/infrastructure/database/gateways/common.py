from sqlalchemy.orm import Session

from src.application.common.interfaces import Commiter


class CommiterImpl(Commiter):
    def __init__(self, session: Session):
        self.session = session

    def commit(self) -> None:
        self.session.commit()
