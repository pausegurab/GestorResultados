from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.temporades import Temporada, TemporadaCreate
from app.crud.temporades import create_temporada as create_temporada_crud
from app.crud.temporades import get_temporades as get_temporades_crud
from app.crud.temporades import get_temporades_by_id as get_temporades_by_id_crud
from app.crud.temporades import get_temporada_by_id as get_temporada_by_id_crud
from app.crud.temporades import delete_temporada as delete_temporada_crud 

router = APIRouter()


@router.post("/", response_model=Temporada)
def create_temporada(temporada_in: TemporadaCreate, db: Session = Depends(get_db)):
    print(f"Creating temporada: {temporada_in}")
    temporada_result = create_temporada_crud(db=db, temporada_in=temporada_in)
    return temporada_result

@router.get("/", response_model=list[Temporada])
def get_temporades(*, db: Session = Depends(get_db)):
    temporades = get_temporades_crud(db=db)
    return [
        Temporada(
            id=t.id,
            any_inici=t.any_inici,
            any_fi=t.any_fi,
            competicio_id=t.competicio_id,
            numero_equips=t.numero_equips
        ) for t in temporades
    ]
@router.get("/competicio/{competicio_id}")
def get_temporades_by_competicio_id(
    competicio_id: int, db: Session = Depends(get_db)):
    temporades = get_temporades_by_id_crud(db=db, competicio_id=competicio_id)
    if not temporades:
        return None
    return [
        Temporada(
            id=t.id,
            any_inici=t.any_inici,
            any_fi=t.any_fi,
            competicio_id=t.competicio_id,
            numero_equips=t.numero_equips
        ) for t in temporades
    ]

@router.get("/{temporada_id}", response_model=Temporada)
def get_temporada_by_id(temporada_id: int, db: Session = Depends(get_db)):
    temporada = get_temporada_by_id_crud(db=db, temporada_id=temporada_id)
    if not temporada:
        return None
    return Temporada(
        id=temporada.id,
        any_inici=temporada.any_inici,
        any_fi=temporada.any_fi,
        competicio_id=temporada.competicio_id,
        numero_equips=temporada.numero_equips
    )

@router.delete("/{temporada_id}", response_model=Temporada)
def delete_temporada(temporada_id: int, db: Session = Depends(get_db)):
    temporada = get_temporada_by_id_crud(db=db, temporada_id=temporada_id)
    if not temporada:
        raise HTTPException(status_code=404, detail="Temporada no trobada")
    deleted_temporada = delete_temporada_crud(db=db, temporada_id=temporada_id)
    return Temporada(
        id=temporada.id,
        any_inici=temporada.any_inici,
        any_fi=temporada.any_fi,
        competicio_id=temporada.competicio_id,
        numero_equips=temporada.numero_equips
    )