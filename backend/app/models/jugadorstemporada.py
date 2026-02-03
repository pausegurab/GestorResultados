from sqlalchemy import Boolean, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class JugadorEquipTemporada(Base):
    __tablename__ = 'jugadors_equips_temporades'

    id = Column(Integer, primary_key=True)

    jugador_id = Column(Integer, ForeignKey('jugadors.id'), nullable=False)
    equip_id = Column(Integer, ForeignKey('equips.id'), nullable=False)
    temporada_id = Column(Integer, ForeignKey('temporades.id'), nullable=False)
    dorsal = Column(Integer, nullable=True)
    dorsal_start_jornada = Column(Integer, nullable=True)
    dorsal_end_jornada = Column(Integer, nullable=True)
    active = Column(Boolean, default=True, nullable=False)

    jugador = relationship("Jugador", back_populates="equips_temporades")
    equip = relationship("Equip", back_populates="jugadors_temporada")
    temporada = relationship("Temporada", back_populates="jugadors_temporada")
