from functools import partial

from sqlalchemy.orm import joinedload
from telebot import TeleBot
from telebot.types import Message

from lib.constants import Constants
from lib.db import get_db_session
from lib.otp_handler import OtpHandler
from lib.wake_on_lan import WakeOnLan
from models import Device, User
from telegram.callbacks.base_callback import BaseCallback


class DeviceSelectedCallback(BaseCallback):
    id = "device"
    has_otp_validation = Constants.HAS_OTP_VALIDATION.lower() in ["1", "true"]

    @classmethod
    def callback(cls, call, bot: TeleBot):
        with get_db_session() as session:
            telegram_user_id = call.from_user.id
            id_device = int(call.data.split(":")[1])
            user = session.query(User).get(telegram_user_id)
            device = session.query(Device) \
                .options(joinedload(Device.macs)) \
                .filter(
                    Device.id_device == id_device,
                    Device.id_user == telegram_user_id
                ) \
                .first()
            if not device:
                bot.answer_callback_query(
                    call.id,
                    text="❌ Device is invalid or does not belong to you."
                )
                return
            if cls.has_otp_validation:
                if not user or not user.otp_secret:
                    bot.send_message(call.message.chat.id, "❌ User not found.")
                    return
                bot.send_message(
                    call.message.chat.id,
                    f"🔒 Please submit your OTP code to confirm access to '"
                    f"{device.name}'.",
                )
                bot.register_next_step_handler(
                    call.message,
                    partial(cls.verify_otp, bot=bot, user=user, device=device)
                )
            else:
                bot.send_message(
                    call.message.chat.id, f"Waking '{device.name}' on LAN."
                )
                cls.wake_on_lan(device)

    @classmethod
    def wake_on_lan(cls, device: Device):
        for mac in device.macs:
            mac_address = mac.mac_address
            for _ in range(2):
                WakeOnLan(mac_address)

    @classmethod
    def verify_otp(
            cls,
            message: Message,
            device: Device,
            user: User,
            bot: TeleBot
    ):
        otp = message.text.strip()
        top_handler = OtpHandler(user.otp_secret, user.name)
        if top_handler.verify(otp):
            bot.send_message(message.chat.id, "✅ Valid OTP. Waking PC on LAN.")
            cls.wake_on_lan(device)
        else:
            bot.send_message(
                message.chat.id,
                "❌ Invalid OTP. Please try again from /start."
            )
