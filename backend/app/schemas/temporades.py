from pydantic import BaseModel, ConfigDict

class TemporadaBase(BaseModel):
    any_inici: int
    any_fi: int
    competicio_id: int
    numero_equips: int

class TemporadaCreate(TemporadaBase):
    pass

class Temporada(TemporadaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)