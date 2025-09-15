from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.paissos import PaisSchema
from app.models.paissos import Pais

router = APIRouter()

@router.get("/", response_model=List[PaisSchema])
def get_paisos(db: Session = Depends(get_db)):
    return db.query(Pais).order_by(Pais.nom.asc()).all()

@router.get("/{pais_id}", response_model=PaisSchema)
def get_pais_by_id(pais_id: int, db: Session = Depends(get_db)):
    pais = db.query(Pais).filter(Pais.id == pais_id).first()
    if not pais:
        raise HTTPException(status_code=404, detail="País no trobat")
    return pais