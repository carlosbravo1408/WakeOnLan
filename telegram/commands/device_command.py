from telebot import TeleBot
from telebot.types import Message, User

from lib.db import get_db_session
from telegram.commands.base_command import BaseCommand


class DeviceCommand(BaseCommand):

    command_list = ["devices"]

    @classmethod
    def callback(cls, message: Message, bot: TeleBot):
        chat_user_id = message.from_user.id
        with get_db_session() as session:
            user = session.query(User).get(chat_user_id)
