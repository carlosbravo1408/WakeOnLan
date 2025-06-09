from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class User(BaseModel):
    id_user = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    otp_secret = Column(String, nullable=False)
    otp_qr_generated = Column(Boolean, default=False, nullable=False)

    devices = relationship(
        "Device",
        back_populates="user",
        cascade="all, delete-orphan"
    )
