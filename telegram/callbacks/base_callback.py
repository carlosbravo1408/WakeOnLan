from telebot import TeleBot
from telebot.types import CallbackQuery


class BaseCallback:
    id: str

    @classmethod
    def callback(cls, query: CallbackQuery, bot: TeleBot) -> None:
        raise NotImplementedError()

    @classmethod
    def register(cls, bot: TeleBot):
        bot.register_callback_query_handler(
            callback=cls.callback,
            func=lambda call: call.data.startswith(f"{cls.id}:"),
            pass_bot=True
        )
