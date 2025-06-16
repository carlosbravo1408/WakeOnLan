from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class SmartPlug(BaseModel):
    __tablename__ = 'smart_plug'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    series = Column(String, nullable=False)
    id_user = Column(
        Integer,
        ForeignKey("user.id_user", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    user = relationship("User", back_populates="smart_plugs")
    device = relationship("Device", back_populates="smart_plug", uselist=False)
