from pydantic import BaseModel, ConfigDict

class EquipBase(BaseModel):
    nom: str
    sigles: str
    pais_id: int
    foto: str     

class EquipCreate(EquipBase):
    pass

class EquipSchema(EquipBase):
    id: int

    model_config = ConfigDict(from_attributes=True)