from typing import List

from telebot import TeleBot
from telebot.types import Message


class BaseCommand:
    command_list: List[str]

    @classmethod
    def callback(cls, message: Message, bot: TeleBot):
        raise NotImplementedError()

    @classmethod
    def register(cls, bot: TeleBot):
        bot.register_message_handler(
            callback=cls.callback,
            commands=cls.command_list,
            pass_bot=True,
        )
