from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import date
from app.models.jugadors import PosicioEnum

class JugadorBase(BaseModel):
    nom: str
    cognom_1: str
    cognom_2: Optional[str] = None
    sobrenom: Optional[str] = None
    posicio: PosicioEnum
    nacionalitat: Optional[int] = None
    url_imatge: Optional[str] = None
    data_naixement: Optional[date] = None

class JugadorCreate(JugadorBase):
    pass

class JugadorSchema(JugadorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class JugadorUpdate(BaseModel):
    nom: Optional[str] = None
    cognom_1: Optional[str] = None
    cognom_2: Optional[str] = None
    sobrenom: Optional[str] = None
    posicio: Optional[PosicioEnum] = None
    nacionalitat: Optional[int] = None
    url_imatge: Optional[str] = None
    data_naixement: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)