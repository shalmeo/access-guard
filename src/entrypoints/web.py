import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telebot import TeleBot

from src.application.ioc import InteractorFactory
from src.config import BotConfig, DatabaseConfig
from src.presentation.web_api.auth import HttpAuthenticator
from src.presentation.web_api.login.router import index_router
from src.presentation.web_api.providers import bot_provider, http_authenticator, ioc, session, session_provider
from src.presentation.web_api.user_profile.router import user_profile_router
from src.presentation.web_api.user_update.router import user_update_router


def main() -> None:
    database_config = DatabaseConfig()
    bot_config = BotConfig()

    api = FastAPI()
    bot = TeleBot(bot_config.token)
    engine = create_engine(url=database_config.uri)
    session_factory = sessionmaker(engine, autoflush=False, expire_on_commit=False)

    api.dependency_overrides[session_provider] = session(session_factory)
    api.dependency_overrides[bot_provider] = lambda: bot
    api.dependency_overrides[InteractorFactory] = ioc
    api.dependency_overrides[HttpAuthenticator] = http_authenticator

    api.include_router(index_router)
    api.include_router(user_profile_router)
    api.include_router(user_update_router)

    config = uvicorn.Config(api)
    server = uvicorn.Server(config)
    server.run()
