from typing import Type

from telebot import TeleBot, logging

from lib.custom_logger import get_logger
from telegram.CustomExceptionHandler import TelegramBotExceptionHandler
from telegram.callbacks.base_callback import BaseCallback
from telegram.commands.base_command import BaseCommand


class TelegramBot:
    def __init__(self, token: str) -> None:
        self._token = token.strip()
        self.__log = get_logger(__name__)
        self._bot = TeleBot(
            token=self._token,
            parse_mode="HTML",
            exception_handler=TelegramBotExceptionHandler(token=self._token)
        )


    def start_polling(self) -> None:
        self.__log.info("Starting Telegram Bot...")
        self._bot.infinity_polling(
            logger_level=logging.DEBUG,
            timeout=30,
            long_polling_timeout=35
        )

    def kill(self):
        self.__log.info("Killing Telegram Bot...")
        self._bot.stop_bot()

    def register_command(self, command: Type[BaseCommand]):
        command.register(self._bot)

    def register_callback(self, callback: Type[BaseCallback]):
        callback.register(self._bot)
