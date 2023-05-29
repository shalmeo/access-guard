from fastapi import FastAPI

from src.application.ioc import InteractorFactory
from src.config import DatabaseConfig
from src.presentation.web_api.auth import HttpAuthenticator
from src.presentation.web_api.login.router import index_router
from src.presentation.web_api.providers import http_authenticator, ioc, session, session_provider
from src.presentation.web_api.user_profile.router import user_profile_router
from src.presentation.web_api.user_update.router import user_update_router


def create_app() -> FastAPI:
    database_config = DatabaseConfig()

    api = FastAPI()

    api.dependency_overrides[session_provider] = session(uri=database_config.uri)
    api.dependency_overrides[InteractorFactory] = ioc
    api.dependency_overrides[HttpAuthenticator] = http_authenticator

    api.include_router(index_router)
    api.include_router(user_profile_router)
    api.include_router(user_update_router)

    return api


app = create_app()
