from fastapi import HTTPException
from app.models.participacions import Participacio
from app.models.temporades import Temporada
from app.models.fases import FaseCompeticio   
from app.schemas.participacions import ParticipacioCreate, ParticipacioSchema
from sqlalchemy.orm import Session

def create_participacio(db: Session, participacio: ParticipacioCreate) -> Participacio:
    temporada = db.query(Temporada).filter(
        Temporada.id == participacio.temporada_id,).first()
    
    
    participacions_actuals = db.query(Participacio).filter(
        Participacio.temporada_id == participacio.temporada_id
    ).count()

    if participacions_actuals >= temporada.numero_equips:
        raise HTTPException(
            status_code=400,
            detail=f"No es poden afegir més equips. El màxim és {temporada.numero_equips}."
        )
    
    db_participacio = Participacio(equip_id=participacio.equip_id,
                                   temporada_id=participacio.temporada_id,)
    db.add(db_participacio)
    db.commit()
    db.refresh(db_participacio)
    return db_participacio

def delete_participacio(db: Session, participacio_id: int) -> Participacio:
    participacio = db.query(Participacio).filter(Participacio.id == participacio_id).first()
    if not participacio:
        return None
    db.delete(participacio)
    db.commit()
    return participacio

def get_participacions(db: Session) -> list[Participacio]:
    participacions = db.query(Participacio).all()
    return participacions

def delete_by_equip_and_temporada(db: Session, equip_id: int, temporada_id: int) -> Participacio:
    participacio = db.query(Participacio).filter(
        Participacio.equip_id == equip_id,
        Participacio.temporada_id == temporada_id
    ).first()
    
    if not participacio:
        return None
    
    db.delete(participacio)
    db.commit()
    return participacio 

def get_temporada_by_fase_id(db: Session, fase_id: int) -> Temporada:
    temporada_id = db.query(FaseCompeticio).filter(
        FaseCompeticio.id == fase_id
    ).first()
    
    
    return temporada_id