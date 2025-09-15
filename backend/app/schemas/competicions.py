import base64
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.competicions import TipusCompeticioEnum

class CompeticioSchema(BaseModel):
    id: int
    nom: str
    tipus: TipusCompeticioEnum
    foto: Optional[str] = None  # base64 string
    pais_id: int

    model_config = ConfigDict(from_attributes=True)

class CompeticioCreate(BaseModel):
    nom: str
    tipus: TipusCompeticioEnum
    foto: Optional[str] = None
    pais_id: int

class CompeticioUpdate(BaseModel):
    nom: Optional[str] = None
    tipus: Optional[TipusCompeticioEnum] = None
    foto: Optional[str] = None
    pais_id: Optional[int] = None

class CompeticioResponse(BaseModel):
    id: int
    nom: str
    foto: Optional[str] = None  # base64 string per a la resposta
    pais_id: int