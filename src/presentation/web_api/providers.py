from typing import Callable

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.application.ioc import IoC
from src.infrastructure.auth.http import HttpAuthenticatorImpl
from src.infrastructure.database.gateways.session import AuthSessionGatewayImpl
from src.infrastructure.database.gateways.user import UserGatewayImpl


def session_provider() -> Session:
    ...


def session(uri: str) -> Callable[[str], Session]:
    engine = create_engine(url=uri)
    session_factory = sessionmaker(engine, expire_on_commit=False)

    def session_wrapper() -> Session:
        session_: Session = session_factory()
        try:
            yield session_
        finally:
            session_.close()

    return session_wrapper


def ioc(session_: Session = Depends(session_provider)):
    return IoC(user_db_gateway=UserGatewayImpl(session=session_))


def http_authenticator(session_: Session = Depends(session_provider)):
    return HttpAuthenticatorImpl(AuthSessionGatewayImpl(session=session_))
