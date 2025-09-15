from pydantic import BaseModel, ConfigDict

class ParticipacioBase(BaseModel):
    temporada_id: int
    equip_id: int

class ParticipacioCreate(ParticipacioBase):
    pass

class ParticipacioSchema(ParticipacioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)