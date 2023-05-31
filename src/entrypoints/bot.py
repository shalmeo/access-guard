from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telebot import TeleBot
from telebot.types import Message

from src.application.auth.dto import TelegramLoginResultDTO
from src.application.auth.usecase import AuthenticateTelegram
from src.config import BotConfig, DatabaseConfig
from src.domain.user import UserId
from src.infrastructure.database.gateways.user import UserGatewayImpl


def extract_user_id(text):
    return text.split()[1] if len(text.split()) > 1 else None


def main():
    print("Bot starting")
    bot_config = BotConfig()
    database_config = DatabaseConfig()

    bot = TeleBot(bot_config.token)
    engine = create_engine(url=database_config.uri)
    session_factory = sessionmaker(engine, autoflush=False, expire_on_commit=False)

    @bot.message_handler(commands=["start"])
    def on_cmd_start(message: Message):
        with session_factory() as session:
            user_id = extract_user_id(message.text)
            AuthenticateTelegram(db_gateway=UserGatewayImpl(session))(
                TelegramLoginResultDTO(user_id=UserId(user_id), telegram_id=message.from_user.id)
            )

    try:
        bot.infinity_polling()
    finally:
        print("Bot stopped")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bot stopped")
