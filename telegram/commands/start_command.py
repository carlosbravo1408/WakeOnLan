import threading

from sqlalchemy.orm import Session
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from lib.constants import Constants
from lib.db import get_db_session
from lib.otp_handler import OtpHandler
from lib.qr_generator import generate_qr
from models import User
from telegram.commands.base_command import BaseCommand


OTP_SECRET_MESSAGE = "🔐 Your OTP secret is:\n||{" \
    "otp_secret}||\n\n⚠️ This message will be deleted in 1 minute"
QR_OTP_SECRET_MESSAGE = "🔐 Or Scan this QR to configure your " \
    "authenticator. \n\n⚠️ This message will be deleted in 1 minute"
USER_NOT_FOUND_MESSAGE = "❌ You shouldn't be here: User not found"
DEVICE_SELECTION_MESSAGE = "👋 Welcome: {name}!\n\n📱 Select a device:"



class StartCommand(BaseCommand):

    command_list = ["start"]
    has_otp = Constants.HAS_OTP_VALIDATION.lower() in ["1", "true"]

    @classmethod
    def callback(cls, message: Message, bot: TeleBot):
        chat_user_id = message.from_user.id
        with get_db_session() as session:
            user = session.query(User).get(chat_user_id)
            if user is None:
                _message = USER_NOT_FOUND_MESSAGE
                markup = None
            else:
                if cls.has_otp and not user.otp_qr_generated:
                    cls._send_otp_secret(message, bot, user, session)
                    return
                _message = DEVICE_SELECTION_MESSAGE.format(name=user.name)
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

    @classmethod
    def _delete_message(cls, bot: TeleBot, message: Message, response: Message):
        if response is not None:
            bot.delete_message(
                message.chat.id,
                response.message_id
            )

    @classmethod
    def _send_otp_secret(
            cls,
            message: Message,
            bot: TeleBot,
            user: User,
            session: Session
    ):
        otp = OtpHandler(user.otp_secret, user.name)
        otp_msg = bot.send_message(
            message.chat.id,
            OTP_SECRET_MESSAGE.format(otp_secret=user.otp_secret),
            parse_mode="MarkdownV2"
        )
        qr_msg = None
        qr_bytes = generate_qr(otp.get_uri())
        if qr_bytes:
            qr_msg = bot.send_photo(
                message.chat.id,
                qr_bytes,
                caption=QR_OTP_SECRET_MESSAGE
            )
        user.otp_qr_generated = True
        session.commit()
        def delete_msgs():
            try:
                cls._delete_message(bot, message, qr_msg)
                cls._delete_message(bot, message, otp_msg)
            except Exception:  #noqa
                pass

        threading.Timer(60.0, delete_msgs).start()
