from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.schemas.participacions import ParticipacioCreate, ParticipacioSchema
from app.schemas.equips import EquipSchema

from app.models.fases import FaseCompeticio
from app.models.classificacions import Classificacio

from app.crud.temporades import get_temporada_by_id as get_temporada_by_id_crud
from app.crud.equip import get_equip_by_id as get_equip_by_id_crud
from app.crud.participacio import create_participacio as create_participacio_crud
from app.crud.participacio import delete_participacio as delete_participacio_crud
from app.crud.equip import get_equips_by_temporada as get_equips_by_temporada_crud
from app.crud.participacio import get_participacions as get_participacions_crud
from app.crud.participacio import delete_by_equip_and_temporada


router = APIRouter()

@router.post("/", response_model=ParticipacioSchema)
def create_participacio(participacio: ParticipacioCreate, db: Session = Depends(get_db)):
   print(f"Received participacio: {participacio}")
   equip_id = participacio.equip_id
   temporada_id = participacio.temporada_id
   print(f"Creating participacio with equip_id: {equip_id}, temporada_id: {temporada_id}")
   temporada = get_temporada_by_id_crud(db, temporada_id)
   if not temporada:
       raise HTTPException(status_code=404, detail="Temporada not found")
   equip = get_equip_by_id_crud(db, equip_id)
   if not equip:
       raise HTTPException(status_code=404, detail="Equip not found")
   particpacio = create_participacio_crud(db, participacio)
   return ParticipacioSchema(id=particpacio.id,
                             equip_id=particpacio.equip_id,
                             temporada_id=particpacio.temporada_id)


@router.delete("/{participacio_id}", response_model=ParticipacioSchema)
def delete_participacio(participacio_id: int, db: Session = Depends(get_db)):
    participacio = delete_participacio_crud(db, participacio_id)
    if not participacio:
        raise HTTPException(status_code=404, detail="Participacio not found")
    return ParticipacioSchema(id=participacio.id,
                             equip_id=participacio.equip_id,
                             temporada_id=participacio.temporada_id)

@router.get("/{temporada_id}/equips", response_model=list[EquipSchema])
def get_equips_by_temporada(temporada_id: int, db: Session = Depends(get_db)):
    temporada = get_temporada_by_id_crud(db, temporada_id)
    if not temporada:
        raise HTTPException(status_code=404, detail="Temporada not found")
    
    equips = get_equips_by_temporada_crud(db, temporada_id)
    return equips

@router.get("/", response_model=list[ParticipacioSchema])
def get_participacions(db: Session = Depends(get_db)):
    participacions = get_participacions_crud(db)    
    if not participacions:
        raise HTTPException(status_code=404, detail="No participacions found")
    return participacions

@router.delete("/{temporada_id}/equips/{equip_id}", response_model=ParticipacioSchema)
def delete_participacio_by_equip(temporada_id: int, equip_id: int, db: Session = Depends(get_db)):

    fases = db.query(FaseCompeticio.id).filter(FaseCompeticio.temporada_id == temporada_id).all()
    fase_ids = [f.id for f in fases]

    if fase_ids:
        db.query(Classificacio).filter(
            Classificacio.equip_id == equip_id,
            Classificacio.fase_id.in_(fase_ids)
        ).delete(synchronize_session=False)

    
    participacio = delete_by_equip_and_temporada(db, equip_id, temporada_id)
    if not participacio:
        raise HTTPException(status_code=404, detail="Participacio not found")
    return ParticipacioSchema(id=participacio.id,
                             equip_id=participacio.equip_id,
                             temporada_id=participacio.temporada_id)