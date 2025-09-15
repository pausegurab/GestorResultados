import enum
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class TipusFaseEnum(enum.Enum):
    LLIGA = "lliga"
    ELIMINATORIA = "eliminatoria"

class FaseCompeticio(Base):
    __tablename__ = 'fases_competicions'
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    tipus = Column(Enum(TipusFaseEnum), nullable=False)
    ordre = Column(Integer, nullable=False)

    temporada_id = Column(Integer, ForeignKey('temporades.id'), nullable=False)
    temporada = relationship("Temporada", back_populates="fases")

    partits = relationship("Partit", back_populates="fase", cascade="all, delete-orphan")
    classificacions = relationship("Classificacio", back_populates="fase",cascade="all, delete")