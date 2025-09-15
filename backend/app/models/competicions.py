import enum
from sqlalchemy import (
    Column, Integer, LargeBinary, String, ForeignKey, Date, Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class TipusCompeticioEnum(enum.Enum):
    LLIGA = "lliga"
    COPA = "copa"
    MIXTE = "mixte"


class Competicio(Base):
    __tablename__ = 'competicions'
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), unique=True, nullable=False)
    tipus = Column(Enum(TipusCompeticioEnum), nullable=False)
    foto = Column(String(255), nullable=True)
    pais_id = Column(Integer, ForeignKey('paissos.id'), nullable=True)

    pais = relationship("Pais", back_populates="competicions")
    temporades = relationship("Temporada", back_populates="competicio")









