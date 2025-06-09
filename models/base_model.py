import re

from sqlalchemy.orm import declarative_base, declared_attr, InstrumentedAttribute


base = declarative_base()


class BaseModel(base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return re.compile(r'(?<!^)(?=[A-Z])').sub('_', cls.__name__).lower()

    @classmethod
    def get_primary_column(cls) -> InstrumentedAttribute:
        return getattr(cls, f"id_{cls.__tablename__}")