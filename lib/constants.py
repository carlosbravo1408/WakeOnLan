import os
import threading

from dotenv import load_dotenv


class _Constants:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, dotenv_path: str = ".env"):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._load(dotenv_path)
            return cls._instance

    def _load(self, dotenv_path: str = ".env"):
        load_dotenv(dotenv_path)
        self.__vars = dict(os.environ)

    def get(self, key: str, default=None):
        return self.__vars.get(key, default)

    def __getattr__(self, key: str):
        return self.get(key)

Constants = _Constants()