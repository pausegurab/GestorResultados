from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Pais(Base):
    __tablename__ = 'paissos'
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False, unique=True)
    url_imatge = Column(String(255), nullable=True)

    equips = relationship("Equip", back_populates="pais")
    competicions = relationship("Competicio", back_populates="pais")

