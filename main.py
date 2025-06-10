import os

from lib.constants import Constants
from lib.db import DataBase
from telegram.callbacks.device_selected_callback import DeviceSelectedCallback
from telegram.commands.device_command import DeviceCommand
from telegram.commands.start_command import StartCommand
from telegram.telegram_bot import TelegramBot


if __name__ == "__main__":
    DataBase()
    bot = TelegramBot(Constants.TELEGRAM_TOKEN)
    bot.register_command(StartCommand)
    bot.register_command(DeviceCommand)
    bot.register_callback(DeviceSelectedCallback)
    try:
        bot.start_polling()
    except KeyboardInterrupt:
        bot.kill()
