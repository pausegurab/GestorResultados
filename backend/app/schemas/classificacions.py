from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ClassificacioBase(BaseModel):
    fase_id: int
    equip_id: int
    jornada: int
    partits_guanyats: int
    partits_empats: int
    partits_perduts: int
    punts: int
    gols_favor: int
    gols_contra: int


class ClassificacioCreate(ClassificacioBase):
    pass

class ClassificacioUpdate(BaseModel):

    fase_id: Optional[int] = None
    equip_id: Optional[int] = None
    jornada: Optional[int] = None
    partits_guanyats: Optional[int] = None
    partits_empats: Optional[int] = None
    partits_perduts: Optional[int] = None
    punts: Optional[int] = None
    gols_favor: Optional[int] = None
    gols_contra: Optional[int] = None

class ClassificacioSchema(ClassificacioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)