from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PartitBase(BaseModel):
    fase_id: int
    jornada: int
    data: Optional[date] = None
    equip_local_id: int
    equip_visitant_id: int
    gols_local: Optional[int] = None
    gols_visitant: Optional[int] = None
    partit_anada_id: Optional[int] = None 


class PartitCreate(PartitBase):
    pass


class PartitUpdate(BaseModel):
    gols_local: Optional[int] = None
    gols_visitant: Optional[int] = None

class PartitSchema(PartitBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class PartitsResultatResponse(BaseModel):
    equips: List[int]
    resultats: List[List[str | None]]