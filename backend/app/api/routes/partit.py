from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.schemas.partits import PartitSchema, PartitCreate, PartitUpdate, PartitsResultatResponse
from app.crud.partit import (create_partit as create_partit_crud, get_partits as get_partits_crud, get_partits_by_jornada as get_partits_by_jornada_crud,
                             get_partit_by_id as get_partit_by_id_crud,
                             update_result as update_result_crud)


from app.crud.equip import get_equips_by_temporada as get_equips_by_temporada_crud
from app.crud.participacio import get_temporada_by_fase_id
from app.services.classificacio_utils import revertir_classificacio, update_classificacio
from app.models.partits import Partit
from app.models.equips import Equip

router = APIRouter()

@router.post("/", response_model=PartitSchema)
def create_partit(partit_in: PartitCreate, db: Session = Depends(get_db)):
    partit = create_partit_crud(partit_in=partit_in, db=db)

    return partit

@router.get("/",response_model=list[PartitSchema])
def get_partits(db: Session = Depends(get_db)):
    partits = get_partits_crud(db=db)
    return [
        PartitSchema(
            id=p.id,
            fase_id=p.fase_id,
            jornada=p.jornada,
            data=p.data,
            equip_local_id=p.equip_local_id,
            equip_visitant_id=p.equip_visitant_id,
            gols_local=p.gols_local,
            gols_visitant=p.gols_visitant,
            partit_anada_id=p.partit_anada_id
        )
        for p in partits
    ]

@router.get("/{fase_id}/jornada/{jornada}", response_model=list[PartitSchema])
def get_partits_by_jornada(fase_id: int, jornada: int, db: Session = Depends(get_db)):
    partits = get_partits_by_jornada_crud(fase_id=fase_id,jornada=jornada,db=db)
    return [
        PartitSchema(
            id=p.id,
            fase_id=p.fase_id,
            jornada=p.jornada,
            data=p.data,
            equip_local_id=p.equip_local_id,
            equip_visitant_id=p.equip_visitant_id,
            gols_local=p.gols_local,
            gols_visitant=p.gols_visitant,
            partit_anada_id=p.partit_anada_id
        )
        for p in partits
    ]

@router.delete("{id}", response_model=PartitSchema)
def delete_partit(id:int, db:Session = Depends(get_db)):
    partit = get_partit_by_id_crud(id,db)
    db.delete(partit)
    db.commit()
    return partit

@router.get("/{id}", response_model=PartitSchema)
def get_partit_by_id(id:int, db: Session = Depends(get_db)):
    partit = get_partit_by_id_crud(id=id,db=db)
    return partit

@router.put("/{id}/gols", response_model=PartitSchema)
def update_result(partit_result: PartitUpdate, id:int, db: Session = Depends(get_db)):
    partit = get_partit_by_id_crud(id=id, db=db)
    if partit is None:
        raise HTTPException(status_code=404, detail="Partit no existent")
    if partit.gols_local is not None and partit.gols_visitant is not None:
        revertir_classificacio(partit_antic=partit, db=db)

        
    partit_updated = update_result_crud(partit_result=partit_result,id=id,db=db)

    updated_classificacio = update_classificacio(partit_updated=partit_updated,db=db)

    return partit_updated

@router.get("/quadre/{fase_id}", response_model=PartitsResultatResponse)
def get_partits_by_temporada(fase_id: int, db: Session = Depends(get_db)):
    partits = db.query(Partit).filter(Partit.fase_id == fase_id).all()
    if not partits:
        raise HTTPException(status_code=404, detail="No s'han trobat partits per aquesta temporada")


    temporada = get_temporada_by_fase_id(db,fase_id)
    temporada_id = temporada.temporada_id
    equips = get_equips_by_temporada_crud(db, temporada_id)

    equips_ord = [e.nom for e in equips]
    equips_ids_ord = [e.id for e in equips]

    n = len(equips)
    taula_resultats = [[None] * n for _ in range(n)]

    id_to_index = {equip_id: idx for idx, equip_id in enumerate(equips_ids_ord)}

    for p in partits:
        i = id_to_index[p.equip_local_id]
        j = id_to_index[p.equip_visitant_id]
        taula_resultats[i][j] = f"{p.gols_local}-{p.gols_visitant}"

    return PartitsResultatResponse(equips=equips_ids_ord, resultats=taula_resultats)
