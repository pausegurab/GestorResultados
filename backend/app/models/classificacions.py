import enum
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class Classificacio(Base):
    __tablename__ = 'classificacions'
    id = Column(Integer, primary_key=True)
    fase_id = Column(Integer, ForeignKey('fases_competicions.id', ondelete="CASCADE"), nullable=False)
    equip_id = Column(Integer, ForeignKey('equips.id'), nullable=False)
    jornada = Column(Integer, nullable=False)

    partits_guanyats = Column(Integer, nullable=False)
    partits_empats = Column(Integer, nullable=False)    
    partits_perduts = Column(Integer, nullable=False)
    punts = Column(Integer, nullable=False)
    gols_favor = Column(Integer, nullable=False)
    gols_contra = Column(Integer, nullable=False)

    fase = relationship("FaseCompeticio", back_populates="classificacions")
    equip = relationship("Equip", back_populates="classificacions")

    __table_args__ = (
        UniqueConstraint('fase_id', 'equip_id', 'jornada', name='uq_classificacio_fase'),
    )