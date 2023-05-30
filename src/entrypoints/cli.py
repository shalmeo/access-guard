import sys
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.application.user.dto import CreateUserDTO
from src.application.user.usecase import CreateUser, GetUsers
from src.config import DatabaseConfig
from src.infrastructure.database.gateways.user import UserGatewayImpl

COMMANDS = ("add", "show")


def main():
    database_config = DatabaseConfig()
    engine = create_engine(url=database_config.uri)
    session_factory = sessionmaker(engine, expire_on_commit=False)

    _, command, *values = sys.argv

    if command not in COMMANDS:
        print("Command not found")
        print(f"Availble commands: {COMMANDS}")
        return

    if command == "add":
        with session_factory() as session:
            user_gateway = UserGatewayImpl(session=session)
            name, password, expired_date, expired_time = values
            expired_in = datetime.strptime(f"{expired_date} {expired_time}", "%d.%m.%Y %H:%M")
            CreateUser(user_gateway)(
                CreateUserDTO(
                    name=name,
                    password=password,
                    expired_in=expired_in,
                )
            )
            expired = "expired!!!" if expired_in < datetime.now() else "active"

            print(f"user successfully added!")
            print(" ")
            print(f"name: {name}")
            print(f"expired in: {expired_in.strftime('%d.%m.%Y %H:%M')} ({expired})")

    if command == "show":
        with session_factory() as session:
            user_gateway = UserGatewayImpl(session=session)
            users = GetUsers(user_gateway)(...)
            for idx, user in enumerate(users, 1):
                expired = "expired!!!" if user.expired else "active"
                print(f"{idx}.")
                print(f"name: {user.name}")
                print(f"expired in: {user.expired_in.strftime('%d.%m.%Y %H:%M')} ({expired})")
                print(" ")


if __name__ == "__main__":
    main()
