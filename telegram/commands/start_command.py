from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from lib.db import get_db_session
from models import User
from telegram.commands.base_command import BaseCommand


class StartCommand(BaseCommand):

    command_list = ["start"]

    @classmethod
    def callback(cls, message: Message, bot: TeleBot):
        chat_user_id = message.from_user.id
        with get_db_session() as session:
            user = session.query(User).get(chat_user_id)
            if user is None:
                _message = "❌ You shouldn't be here: User not found"
                markup = None
            else:
                _message = f"👋 Welcome: {user.name}!\n\n📱 Select a device:"
                markup = InlineKeyboardMarkup()
                for device in user.devices:
                    markup.add(
                        InlineKeyboardButton(
                            text=device.name,
                            callback_data=f"device:{device.id_device}"
                        )
                    )
            bot.reply_to(
                message,
                text=_message,
                reply_parameters=None,
                reply_markup=markup
            )
