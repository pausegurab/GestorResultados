from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class PlantillaBase(BaseModel):
    temporada_id: int
    equip_id: int

class PlantillaCreate(PlantillaBase):
    jugador_ids: List[int]

class Plantilla(PlantillaBase):
    id: int
    jugador_id: int

    model_config = ConfigDict(from_attributes=True)