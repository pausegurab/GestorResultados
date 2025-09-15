from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.fases import FaseCreate, Fase
from app.models.fases import FaseCompeticio

from app.crud.fase import create_fase as create_fase_crud
from app.crud.fase import get_fases as get_fases_crud
from app.crud.fase import get_fase_by_id as get_fase_by_id_crud
from app.crud.fase import get_fases_by_temporada_id as get_fases_by_temporada_id_crud
from app.crud.fase import get_fases_lliga_by_temporada_id as get_fases_lliga_by_temporada_id_crud

router = APIRouter()

@router.post("/", response_model=Fase)
def create_fase(fase_in: FaseCreate, db: Session = Depends(get_db)):
    fase = create_fase_crud(db=db, fase_in=fase_in)
    return fase

@router.get("/", response_model=List[Fase])
def get_fases(db: Session = Depends(get_db)):
    fases = get_fases_crud(db=db)
    if not fases:
        raise HTTPException(status_code=404, detail="No phases found")
    
    return [
        Fase(
            id=t.id,
            nom=t.nom,
            tipus=t.tipus,
            temporada_id=t.temporada_id,
            ordre=t.ordre
        ) for t in fases
    ]

@router.get("/{fase_id}", response_model=Fase)
def get_fase_by_id(fase_id: int, db: Session = Depends(get_db)):
    fase = get_fase_by_id_crud(db=db, fase_id=fase_id)
    if not fase:
        raise HTTPException(status_code=404, detail="Phase not found")
    
    return Fase(
        id=fase.id,
        nom=fase.nom,
        tipus=fase.tipus,
        temporada_id=fase.temporada_id,
        ordre=fase.ordre
    )

@router.get("/temporada/{temporada_id}", response_model=List[Fase])
def get_fases_by_temporada_id(temporada_id: int, db: Session = Depends(get_db)):
    fases = get_fases_by_temporada_id_crud(db=db, temporada_id=temporada_id)
    if not fases:
        raise HTTPException(status_code=404, detail="No phases found for this season")
    
    return [
        Fase(
            id=t.id,
            nom=t.nom,
            tipus=t.tipus,
            temporada_id=t.temporada_id,
            ordre=t.ordre
        ) for t in fases
    ]
@router.get("/lliga/{temporada_id}", response_model=List[Fase])
def get_fases_lliga_by_temporada_id(temporada_id: int, db: Session = Depends(get_db)):
    fases = get_fases_lliga_by_temporada_id_crud(db=db, temporada_id=temporada_id)

    if not fases:
        raise HTTPException(status_code=404, detail="No league phases found for this season")
    
    return [
        Fase(
            id=fase.id,
            nom=fase.nom,
            tipus=fase.tipus,
            temporada_id=fase.temporada_id,
            ordre=fase.ordre
        ) for fase in fases
    ]