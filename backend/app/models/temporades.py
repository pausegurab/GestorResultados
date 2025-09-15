import enum
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Temporada(Base):
    __tablename__ = 'temporades'
    id = Column(Integer, primary_key=True)
    any_inici = Column(Integer, nullable=False)
    any_fi = Column(Integer, nullable=False)
    numero_equips = Column(Integer, nullable=False)
    competicio_id = Column(Integer, ForeignKey('competicions.id'), nullable=False)
    

    competicio = relationship("Competicio", back_populates="temporades")
    equips = relationship("Participacio", back_populates="temporada", cascade="all, delete-orphan")
    fases = relationship("FaseCompeticio", back_populates="temporada", order_by="FaseCompeticio.ordre", cascade="all, delete-orphan")
    jugadors_temporada = relationship("JugadorEquipTemporada", back_populates="temporada", cascade="all, delete-orphan")

