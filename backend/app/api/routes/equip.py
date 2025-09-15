from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.equips import EquipCreate, EquipSchema
from app.models.equips import Equip

from app.crud.equip import get_equips as get_equips_crud
from app.crud.equip import get_equip_by_id as get_equip_by_id_crud
from app.crud.equip import create_equip as create_equip_crud
from app.crud.equip import delete_equip as delete_equip_crud

router = APIRouter()

@router.get("/", response_model=List[EquipSchema])
def get_equips(db: Session = Depends(get_db)):
    equips = get_equips_crud(db)
    if not equips:
        return {"detail": "No equips found"}
    return [EquipSchema(
        id=e.id,
        nom=e.nom,
        sigles=e.sigles,
        pais_id=e.pais_id,
        foto=e.foto
        ) for e in equips]
  

@router.get("/{equip_id}", response_model=EquipSchema)
def get_equip_by_id(equip_id: int, db: Session = Depends(get_db)):
    equip = get_equip_by_id_crud(db, equip_id)
    if not equip:
        raise HTTPException(status_code=404, detail="Equip not found")
    return EquipSchema(
        id=equip.id,
        nom=equip.nom,
        sigles=equip.sigles,
        pais_id=equip.pais_id,
        foto=equip.foto
    )

@router.post("/", response_model=EquipSchema)
def create_equip(equip_in: EquipCreate, db: Session = Depends(get_db)):
    equip = create_equip_crud(db, equip_in)
    if not equip:
        raise HTTPException(status_code=400, detail="Error creating equip")
    return EquipSchema(
        id=equip.id,
        nom=equip.nom,
        sigles=equip.sigles,
        pais_id=equip.pais_id,
        foto=equip.foto
    )

@router.delete("/{equip_id}")
def delete_equip(equip_id: int, db: Session = Depends(get_db)):
    try:
        delete_equip_crud(db, equip_id)
        return {"detail": "Equip deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")