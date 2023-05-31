import time

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from telebot import TeleBot

from src.application.user.usecase import SendNotifications
from src.config import BotConfig, DatabaseConfig, NotificationSenderConfig
from src.infrastructure.database.gateways.user import (SessionGatewayImpl,
                                                       UserGatewayImpl)


def run_notification_sender(
    config: NotificationSenderConfig,
    bot: TeleBot,
    session_factory: sessionmaker[Session],
):
    while True:
        with session_factory() as session:
            SendNotifications(
                user_gateway=UserGatewayImpl(session),
                session_gateway=SessionGatewayImpl(session),
                bot=bot,
            )(...)
            time.sleep(config.check_interval)


def main():
    print("Notification sender starting")
    database_config = DatabaseConfig()
    sender_config = NotificationSenderConfig()
    bot_config = BotConfig()

    bot = TeleBot(bot_config.token, parse_mode="HTML")
    engine = create_engine(database_config.uri)
    session_factory = sessionmaker(engine, autoflush=False, expire_on_commit=False)

    try:
        run_notification_sender(sender_config, bot, session_factory)
    finally:
        engine.dispose()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Notification sender stopped")
