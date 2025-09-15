from app.models.temporades import Temporada 
from app.schemas.temporades import TemporadaCreate
from sqlalchemy.orm import Session


def create_temporada(*, db: Session, temporada_in: TemporadaCreate) -> Temporada:
    db_temporada = Temporada(
        competicio_id=temporada_in.competicio_id,
        any_inici=temporada_in.any_inici,
        any_fi=temporada_in.any_fi,
        numero_equips=temporada_in.numero_equips,
    )
    db.add(db_temporada)
    db.commit()
    db.refresh(db_temporada)
    return db_temporada
    

def get_temporades(db: Session) -> list[Temporada]:
    temporades = db.query(Temporada).all()
    return temporades

def get_temporades_by_id(db: Session, competicio_id: int) -> list[Temporada]:
    temporades = db.query(Temporada).filter(Temporada.competicio_id == competicio_id).all()
    return temporades

def get_temporada_by_id(db: Session, temporada_id: int) -> Temporada:
    temporada = db.query(Temporada).filter(Temporada.id == temporada_id).first()
    return temporada

def delete_temporada(db: Session, temporada_id: int):
    temporada = db.query(Temporada).filter(Temporada.id == temporada_id).first()
    if temporada:
        db.delete(temporada)
        db.commit()
    return {"detail": "Competicio deleted successfully"}