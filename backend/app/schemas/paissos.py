from pydantic import BaseModel, ConfigDict

class PaisSchema(BaseModel):
    id: int
    nom: str
    url_imatge: str