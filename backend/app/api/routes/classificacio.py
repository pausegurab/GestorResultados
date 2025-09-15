from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.schemas.classificacions import ClassificacioCreate, ClassificacioSchema

from app.models.fases import TipusFaseEnum
from app.crud.fase import get_fase_by_id as get_fase_by_id_crud
from app.crud.classificacio import create_classificacio_primera_jornada as create_classificacio_primera_jornada_crud
from app.crud.classificacio import (get_classificacio_by_jornada as get_classificacio_crud, get_classificacio_by_id_crud, delete_classificacio as delete_classificacio_crud)
from app.services.classificacio_utils import ordenar_classificacio
from app.crud.equip import get_equip_by_id as get_equip_by_id_crud
from app.models.classificacions import Classificacio

router = APIRouter()


@router.post("/primera_jornada", response_model=ClassificacioSchema)
def create_classificacio_primera_jornada(fase_id: int,equip_id:int, db: Session = Depends(get_db)):

    fase = get_fase_by_id_crud(db, fase_id)
    
    if not fase:
        raise HTTPException(status_code=404, detail="Fase not found")
    if fase.tipus != TipusFaseEnum.LLIGA:
        raise HTTPException(status_code=400, detail="Only league phases can have a first jornada classification")   

    classificacio_in = ClassificacioCreate(
        fase_id=fase_id,
        equip_id=equip_id,
        jornada=1,
        punts=0,
        partits_guanyats=0,
        partits_empats=0,
        partits_perduts=0,
        gols_favor=0,
        gols_contra=0
    )

    classificacio = create_classificacio_primera_jornada_crud(db, classificacio_in)
    return classificacio
@router.get("/historic/{fase_id}")
def get_classificacio_historic(fase_id: int, db: Session = Depends(get_db)):
    fase = get_fase_by_id_crud(db, fase_id)
    if not fase:
        raise HTTPException(status_code=404, detail="Fase not found")

    if fase.tipus != TipusFaseEnum.LLIGA:
        raise HTTPException(status_code=400, detail="Only league phases can have historic classification")

    jornada_max = db.query(func.max(Classificacio.jornada)).filter_by(fase_id=fase_id).scalar()

    if not jornada_max:
        raise HTTPException(status_code=404, detail="No classifications available")

    equips_posicions = {}
    jornades = []

    for jornada in range(1, jornada_max + 1):
        classificacio = get_classificacio_crud(db, fase_id, jornada)
        if not classificacio:
            continue

        classif_ord = ordenar_classificacio(classificacio, fase_id, db)
        jornades.append(f"J{jornada}")

        for posicio, fila in enumerate(classif_ord, start=1):
            if fila.equip_id not in equips_posicions:
                equips_posicions[fila.equip_id] = []
            equips_posicions[fila.equip_id].append(posicio)

    equips_noms = {}
    for equip_id in equips_posicions:
        equip = get_equip_by_id_crud(db, equip_id)
        equips_noms[equip.nom] = equips_posicions[equip_id]

    return {
        "jornades": jornades,
        "equips": equips_noms
    }


@router.get("/{fase_id}/{jornada}", response_model=list[ClassificacioSchema])
def get_classificacio_by_jornada(fase_id: int, jornada: int, db: Session = Depends(get_db)):
    fase = get_fase_by_id_crud(db, fase_id)
    if not fase:
        raise HTTPException(status_code=404, detail="Fase not found")
    
    if fase.tipus != TipusFaseEnum.LLIGA:
        raise HTTPException(status_code=400, detail="Only league phases can have a first jornada classification")   

    classificacio = get_classificacio_crud(db, fase_id, jornada)
    

    if not classificacio:
        raise HTTPException(status_code=404, detail="Classification for the first jornada not found")


    classif_ord = ordenar_classificacio(classificacio, fase_id, db, jornada)
    
    return [ClassificacioSchema(
        id=c.id,
        fase_id=c.fase_id,
        equip_id=c.equip_id,
        jornada=c.jornada,
        punts=c.punts,
        partits_guanyats=c.partits_guanyats,
        partits_empats=c.partits_empats,
        partits_perduts=c.partits_perduts,
        gols_favor=c.gols_favor,
        gols_contra=c.gols_contra
    ) for c in classif_ord]






@router.delete("/{classificacio_id}", response_model=ClassificacioSchema)
def delete_classificacio_by_id(classificacio_id: int, db: Session = Depends(get_db)):
    classificacio = get_classificacio_by_id_crud(db, classificacio_id)

    if not classificacio:
        raise HTTPException(status_code=404, detail="Classification not found")
    
    result = ClassificacioSchema(
        id=classificacio.id,
        fase_id=classificacio.fase_id,
        equip_id=classificacio.equip_id,
        jornada=classificacio.jornada,
        punts=classificacio.punts,
        partits_guanyats=classificacio.partits_guanyats,
        partits_empats=classificacio.partits_empats,
        partits_perduts=classificacio.partits_perduts,
        gols_favor=classificacio.gols_favor,
        gols_contra=classificacio.gols_contra
    )

    delete_classificacio_crud(db, classificacio)

    return result