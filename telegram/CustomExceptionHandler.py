from telebot import ExceptionHandler

from lib.custom_logger import get_logger


class TelegramBotExceptionHandler(ExceptionHandler):
    def __init__(self, token: str):
        self.__log = get_logger(__name__)
        self._token = token

    def handle(self, exception):
        exception_message = str(exception).replace(self._token, 'xx:xxxxx')
        self.__log.error(exception_message)
        return False

