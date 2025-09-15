from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

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

    # 🟢 Transformem a format Plantilla
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
    plantilla = (
        db.query(Jugador)
        .join(JugadorEquipTemporada, Jugador.id == JugadorEquipTemporada.jugador_id)
        .filter(
            JugadorEquipTemporada.equip_id == equip_id,
            JugadorEquipTemporada.temporada_id == temporada_id
        )
        .all()
    )

    if not plantilla:
        raise HTTPException(status_code=404, detail="Plantilla no trobada")

    return plantilla