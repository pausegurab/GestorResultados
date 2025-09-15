import enum
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Partit(Base):
    __tablename__ = 'partits'
    id = Column(Integer, primary_key=True)
    fase_id = Column(Integer, ForeignKey('fases_competicions.id', ondelete="CASCADE"), nullable=False)
    jornada = Column(Integer, nullable=True)  # només útil si és lliga
    data = Column(Date, nullable=True)

    equip_local_id = Column(Integer, ForeignKey('equips.id'), nullable=False)
    equip_visitant_id = Column(Integer, ForeignKey('equips.id'), nullable=False)

    gols_local = Column(Integer, nullable=True)
    gols_visitant = Column(Integer, nullable=True)

    partit_anada_id = Column(Integer, ForeignKey('partits.id'), nullable=True)

    fase = relationship("FaseCompeticio", back_populates="partits")
    partit_anada = relationship("Partit", remote_side=[id])
    equip_local = relationship("Equip", foreign_keys=[equip_local_id])
    equip_visitant = relationship("Equip", foreign_keys=[equip_visitant_id])
