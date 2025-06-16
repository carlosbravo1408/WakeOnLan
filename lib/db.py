import contextvars
import threading
from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models.base_model import BaseModel


DB = "hgrW8WzeIsqDw5lU.db"
_current_session = contextvars.ContextVar("current_session", default=None)


class DataBase:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_url: str = f"sqlite:///{DB}"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.engine = create_engine(
                    db_url,
                    echo=False,
                    connect_args={'check_same_thread': False}
                )
                cls._instance.SessionLocal = sessionmaker(
                    bind=cls._instance.engine, expire_on_commit=False
                )
                BaseModel.metadata.create_all(cls._instance.engine)
            return cls._instance

    def get_session(self) -> Session:
        return self.SessionLocal()


@contextmanager
def get_db_session():
    existing_session = _current_session.get()
    if existing_session is not None:
        yield existing_session
        return

    db = DataBase()
    session = db.get_session()
    token = _current_session.set(session)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        _current_session.reset(token)
        session.close()


def db_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        with get_db_session():
            return function(*args, **kwargs)
    return wrapper
