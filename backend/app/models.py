from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Fisherman(Base):
    __tablename__ = "fishermen"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    catches = relationship("Catch", back_populates="fisherman")

class Catch(Base):
    __tablename__ = "catches"
    id = Column(Integer, primary_key=True, index=True)
    fisherman_id = Column(Integer, ForeignKey("fishermen.id"), nullable=True)
    species = Column(String, index=True)
    quantity = Column(Integer)
    size_cm = Column(Float, nullable=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    synced = Column(Boolean, default=True)

    fisherman = relationship("Fisherman", back_populates="catches")
