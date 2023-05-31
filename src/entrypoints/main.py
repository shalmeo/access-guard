import sys
from threading import Thread

from src.entrypoints import bot, notification_sender, web


def main():
    web_thread = Thread(target=web.main, daemon=True)
    sender_thread = Thread(target=notification_sender.main)
    bot_thread = Thread(target=bot.main)

    sender_thread.start()
    bot_thread.start()
    web_thread.start()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
