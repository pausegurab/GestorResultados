import enum
from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class PosicioEnum(enum.Enum):
    POR = "POR"
    DEF = "DEF"
    MIG = "MIG"
    DAV = "DAV"

class Jugador(Base):
    __tablename__ = 'jugadors'
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    cognom_1 = Column(String(100), nullable=False)
    cognom_2 = Column(String(100), nullable=True)
    sobrenom = Column(String(100), nullable=True)
    posicio = Column(Enum(PosicioEnum), nullable=False)
    data_naixement = Column(Date, nullable=True)
    nacionalitat = Column(Integer, ForeignKey('paissos.id'), nullable=True)
    url_imatge = Column(String(255), nullable=True)

    equips_temporades = relationship("JugadorEquipTemporada", back_populates="jugador", cascade="all, delete-orphan")

