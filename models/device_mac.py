from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class DeviceMac(BaseModel):
    __tablename__ = "device_mac"

    id_mac = Column(Integer, primary_key=True, autoincrement=True)
    id_device = Column(Integer,
                       ForeignKey("device.id_device", ondelete="CASCADE",
                                  onupdate="CASCADE"), nullable=False)
    mac_address = Column(String, nullable=False)

    device = relationship("Device", back_populates="macs")
