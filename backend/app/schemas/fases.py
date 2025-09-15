from pydantic import BaseModel, ConfigDict
from enum import Enum

class TipusFaseEnum(str, Enum):
    lliga = "lliga"
    eliminatoria = "eliminatoria"

class FaseCreate(BaseModel):
    nom: str
    tipus: TipusFaseEnum
    ordre: int
    temporada_id: int

class Fase(BaseModel):
    id: int
    nom: str
    tipus: TipusFaseEnum
    ordre: int
    temporada_id: int

    model_config = ConfigDict(from_attributes=True)