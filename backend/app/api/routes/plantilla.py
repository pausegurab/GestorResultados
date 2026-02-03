from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from collections import defaultdict

class AssignDorsalRequest(BaseModel):
    dorsal: Optional[int] = None
    dorsal_start_jornada: Optional[int] = None
    dorsal_end_jornada: Optional[int] = None

from app.models.partits import Partit
from app.models.equips import Equip
from app.models.jugadors import Jugador

from app.schemas.plantilla import Plantilla, PlantillaCreate
from app.models.jugadorstemporada import JugadorEquipTemporada
from app.schemas.jugadors import JugadorSchema

router = APIRouter()

@router.post("/", response_model=List[Plantilla])
def afegir_jugadors_plantilla(plantilla_in: PlantillaCreate, db: Session = Depends(get_db)):
    equip = db.query(Equip).filter(Equip.id == plantilla_in.equip_id).first()
    if not equip:
        raise HTTPException(status_code=404, detail="Equip no trobat")
    
    jugadors_existents = db.query(JugadorEquipTemporada).filter(JugadorEquipTemporada.equip_id == plantilla_in.equip_id).all()
    jugadors_existents_ids = {jugador.jugador_id for jugador in jugadors_existents}
    
    nous_jugadors = []
    for jugador_id in plantilla_in.jugador_ids:
        if jugador_id not in jugadors_existents_ids:
            nou_jugador = JugadorEquipTemporada(
                equip_id=plantilla_in.equip_id,
                jugador_id=jugador_id,
                temporada_id=plantilla_in.temporada_id
            )
            db.add(nou_jugador)
            db.flush()
            db.refresh(nou_jugador)
            nous_jugadors.append(nou_jugador)

    db.commit()

    return [
        Plantilla(
            id=j.id,
            jugador_id=j.jugador_id,
            equip_id=j.equip_id,
            temporada_id=j.temporada_id
        )
        for j in nous_jugadors
    ]


@router.get("/{equip_id}/{temporada_id}", response_model=List[JugadorSchema])
def obtenir_plantilla(equip_id: int, temporada_id: int, db: Session = Depends(get_db)):
    jugadors_equip_temporada = (
        db.query(JugadorEquipTemporada)
        .filter(
            JugadorEquipTemporada.equip_id == equip_id,
            JugadorEquipTemporada.temporada_id == temporada_id
        )
        .all()
    )

    if not jugadors_equip_temporada:
        raise HTTPException(status_code=404, detail="Plantilla no trobada")

    jugadors_dict = defaultdict(list)
    jugador_ids = set()
    ids_plantilla = dict()
    for jet in jugadors_equip_temporada:
        jugador_ids.add(jet.jugador_id)
        ids_plantilla[jet.jugador_id] = jet.id
        if jet.dorsal is not None:
            jugadors_dict[jet.jugador_id].append(jet.dorsal)

    jugadors = db.query(Jugador).filter(Jugador.id.in_(jugador_ids)).all()
    jugadors_by_id = {j.id: j for j in jugadors}

    result = []
    for jugador_id in jugador_ids:
        jugador = jugadors_by_id[jugador_id]
        dorsals = jugadors_dict[jugador_id]
        result.append(JugadorSchema(**jugador.__dict__, dorsals=dorsals, id_plantilla=ids_plantilla[jugador_id]))
    return result

@router.put("/{jugador_equip_temporada_id}/dorsal")
def assignar_dorsal(jugador_equip_temporada_id:int, request: AssignDorsalRequest, db: Session = Depends(get_db)):
    jugador_equip_temporada = db.query(JugadorEquipTemporada).filter(JugadorEquipTemporada.id == jugador_equip_temporada_id).first()
    if not jugador_equip_temporada:
        raise HTTPException(status_code=404, detail="Jugador no trobat en l'equip i temporada especificats")
    
    if jugador_equip_temporada.dorsal is None:
        jugador_equip_temporada.dorsal = request.dorsal
        jugador_equip_temporada.dorsal_start_jornada = request.dorsal_start_jornada
        jugador_equip_temporada.dorsal_end_jornada = request.dorsal_end_jornada
        if request.dorsal_end_jornada is None:  
            jugador_equip_temporada.active = True
        else:
            jugador_equip_temporada.active = False

        db.commit()
        db.refresh(jugador_equip_temporada)
    else:
        nou_jugador_equip_temporada = JugadorEquipTemporada(
            equip_id=jugador_equip_temporada.equip_id,
            jugador_id=jugador_equip_temporada.jugador_id,
            temporada_id=jugador_equip_temporada.temporada_id,
            dorsal=request.dorsal,
            dorsal_start_jornada=request.dorsal_start_jornada,
            dorsal_end_jornada=request.dorsal_end_jornada,
            active=True
        )
        jugador_equip_temporada.active = False
        jugador_equip_temporada.dorsal_end_jornada = request.dorsal_start_jornada - 1
        db.add(nou_jugador_equip_temporada)
        db.commit()
        db.refresh(nou_jugador_equip_temporada)
        db.refresh(jugador_equip_temporada)


    return {"message": "Dorsal assignat correctament"}