import time
from functools import partial

from sqlalchemy.orm import joinedload
from telebot import TeleBot
from telebot.types import Message

from lib.constants import Constants
from lib.db import get_db_session, db_session
from lib.otp_handler import OtpHandler
from lib.smart_plug import create_smart_plug_instance
from lib.wake_on_lan import WakeOnLan
from models import Device, User
from telegram.callbacks.base_callback import BaseCallback


WAKING_MESSAGE = "Device {device} selected, attempting to Wake on Lan"


class DeviceSelectedCallback(BaseCallback):
    id = "device"
    has_otp_validation = Constants.HAS_OTP_VALIDATION.lower() in ["1", "true"]

    @classmethod
    def callback(cls, call, bot: TeleBot):
        with get_db_session():
            telegram_user_id = call.from_user.id
            id_device = int(call.data.split(":")[1])
            cls.remove_interactive_buttons(bot, call.message)
            user = cls._get_user_from_id(telegram_user_id)
            device = cls._get_device_from_id(telegram_user_id, id_device)
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
                    f"🔒 Please submit your OTP code to confirm access to "
                    f"'{device.name}'.",
                )
                bot.register_next_step_handler(
                    call.message,
                    partial(cls.verify_otp, bot=bot, user_id=user.id_user,
                            device_id=device.id_device)
                )
            else:
                bot.send_message(
                    call.message.chat.id, WAKING_MESSAGE.format(
                        device=device.name)
                )
                cls.power_on_smart_plug(device=device)
                cls.wake_on_lan(device)

    @classmethod
    def _get_user_from_id(cls, user_id: int):
        with get_db_session() as session:
            return session.query(User).get(user_id)

    @classmethod
    def _get_device_from_id(cls, user_id: int, device_id: int):
        with get_db_session() as session:
            return session.query(Device) \
                .options(joinedload(Device.macs)) \
                .filter(
                    Device.id_device == device_id,
                    Device.id_user == user_id
                ).first()

    @classmethod
    def power_on_smart_plug(cls, device: Device):
        if device.smart_plug:
            plug = create_smart_plug_instance(
                manufacturer=device.smart_plug.manufacturer,
                series=device.smart_plug.series,
                host=device.smart_plug.ip_address
            )
            if plug.get_relay_state():
                return
            plug.turn_on()
            time.sleep(10)

    @classmethod
    def wake_on_lan(cls, device: Device):
        for mac in device.macs:
            mac_address = mac.mac_address
            for _ in range(2):
                WakeOnLan(mac_address)

    @classmethod
    def remove_interactive_buttons(cls, bot: TeleBot, message: Message):
        bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=None
        )

    @classmethod
    @db_session
    def verify_otp(
            cls,
            message: Message,
            device_id: int,
            user_id: int,
            bot: TeleBot
    ):
        user = cls._get_user_from_id(user_id)
        device = cls._get_device_from_id(user_id, device_id)
        otp = message.text.strip()
        top_handler = OtpHandler(user.otp_secret, user.name)
        if top_handler.verify(otp):
            bot.send_message(
                message.chat.id, "✅ Valid OTP.\n" + WAKING_MESSAGE.format(
                        device=device.name))
            cls.power_on_smart_plug(device)
            cls.wake_on_lan(device)
        else:
            bot.send_message(
                message.chat.id,
                "❌ Invalid OTP. Please try again from /start."
            )
