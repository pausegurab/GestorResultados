import enum
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.core.database import Base

class Equip(Base):
    __tablename__ = 'equips'
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False, unique=True)
    sigles = Column(String(10), nullable=False, unique=False)
    foto = Column(String(255), nullable=True)
    pais_id = Column(Integer, ForeignKey('paissos.id'), nullable=True)

    pais = relationship("Pais", back_populates="equips")
    participacions = relationship("Participacio", back_populates="equip")
    classificacions = relationship("Classificacio", back_populates="equip")
    jugadors_temporada = relationship("JugadorEquipTemporada", back_populates="equip", cascade="all, delete-orphan")