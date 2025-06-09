import threading
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models.base_model import BaseModel


DB = "hgrW8WzeIsqDw5lU.db"


class DataBase:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_url = f"sqlite:///{DB}"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.engine = create_engine(
                    db_url,
                    echo=False,
                    connect_args={'check_same_thread': False}
                )
                cls._instance.SessionLocal = sessionmaker(
                    bind=cls._instance.engine, expire_on_commit=False)
                BaseModel.metadata.create_all(cls._instance.engine)
            return cls._instance

    def get_session(self) -> Session:
        return self.SessionLocal()

@contextmanager
def get_db_session():
    db = DataBase()
    session = db.get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
