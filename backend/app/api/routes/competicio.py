import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.competicions import CompeticioCreate, CompeticioSchema, CompeticioResponse, CompeticioUpdate
from app.crud.competicio import create_competicio as create_competicio_crud
from app.crud.competicio import get_competicions as get_competicions_crud
from app.crud.competicio import get_competicio_by_id
from app.crud.competicio import update_competicio as update_competicio_crud
from app.crud.competicio import delete_competicio as delete_competicio_crud 

router = APIRouter()

@router.get("/", response_model=list[CompeticioSchema])
def get_competicions(*, db: Session = Depends(get_db)):
    competicions = get_competicions_crud(db=db)
    return [
        CompeticioSchema(
            id=c.id,
            nom=c.nom,
            tipus=c.tipus,
            foto=c.foto,
            pais_id=c.pais_id
        ) for c in competicions
    ]

@router.get("/{competicio_id}", response_model=CompeticioSchema)
def get_competicio(*, competicio_id: int, db: Session = Depends(get_db)):
    competicio = get_competicio_by_id(db=db, competicio_id=competicio_id)
    if not competicio:
        raise HTTPException(status_code=404, detail="Competicio not found")
    return CompeticioSchema(
        id=competicio.id,
        nom=competicio.nom,
        tipus=competicio.tipus,
        foto=competicio.foto,
        pais_id=competicio.pais_id
    )

@router.post("/", response_model=CompeticioSchema)
def create_competicio(*, db: Session = Depends(get_db), competicio_in: CompeticioCreate):
    competicio = create_competicio_crud(db=db, competicio_in=competicio_in)
    return CompeticioSchema(
        id=competicio.id,
        nom=competicio.nom,
        tipus=competicio.tipus,
        foto=competicio.foto,
        pais_id=competicio.pais_id
    )

@router.put("/{competicio_id}", response_model=CompeticioSchema)
def update_competicio(
    competicio_id: int,
    competicio_in: CompeticioUpdate,
    db: Session = Depends(get_db)
):
    updated_competicio = update_competicio_crud(db=db, competicio_in=competicio_in, competicio_id=competicio_id)
    return CompeticioSchema(
        id=updated_competicio.id,
        nom=updated_competicio.nom,
        tipus=updated_competicio.tipus,
        foto=updated_competicio.foto,
        pais_id=updated_competicio.pais_id
    )

@router.delete("/{competicio_id}")
def delete_competicio(*, competicio_id: int, db: Session = Depends(get_db)):
    competicio = get_competicio_by_id(db=db, competicio_id=competicio_id)
    if not competicio:
        raise HTTPException(status_code=404, detail="Competicio not found")
    
    delete_result = delete_competicio_crud(db=db, competicio_id=competicio_id)
    return delete_result