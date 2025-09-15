import enum
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class Participacio(Base):
    __tablename__ = 'participacions'
    id = Column(Integer, primary_key=True)
    temporada_id = Column(Integer, ForeignKey('temporades.id'), nullable=False)
    equip_id = Column(Integer, ForeignKey('equips.id'), nullable=False)

    temporada = relationship("Temporada", back_populates="equips")
    equip = relationship("Equip", back_populates="participacions")

    __table_args__ = (
        UniqueConstraint('temporada_id', 'equip_id', name='uq_temporada_equip'),
    )