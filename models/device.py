from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Device(BaseModel):
    id_device = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    id_user = Column(
        Integer,
        ForeignKey(
            "user.id_user",
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        nullable=False,
    )
    id_smart_plug = Column(
        Integer,
        ForeignKey(
            "smart_plug.id",
            ondelete="SET NULL",
            onupdate="CASCADE"
        ),
        nullable=True,
    )

    user = relationship("User", back_populates="devices")
    macs = relationship(
        "DeviceMac", back_populates="device", cascade="all, delete-orphan"
    )
    smart_plug = relationship(
        "SmartPlug",
        back_populates="device",
        uselist=False
    )
