from sqlalchemy.orm import Session
from app.models.classificacions import Classificacio
from app.schemas.classificacions import ClassificacioCreate, ClassificacioSchema

def create_classificacio_primera_jornada(db: Session, classificacio_in: ClassificacioCreate) -> ClassificacioSchema:
    classificacio = Classificacio(
        fase_id=classificacio_in.fase_id,
        equip_id=classificacio_in.equip_id,
        jornada=classificacio_in.jornada,
        punts=classificacio_in.punts,
        partits_guanyats=classificacio_in.partits_guanyats,
        partits_empats=classificacio_in.partits_empats,
        partits_perduts=classificacio_in.partits_perduts,
        gols_favor=classificacio_in.gols_favor,
        gols_contra=classificacio_in.gols_contra
    )
    db.add(classificacio)
    db.commit()
    db.refresh(classificacio)
    return ClassificacioSchema.model_validate(classificacio)

def get_classificacio_by_jornada(db: Session, fase_id: int, jornada: int):
    classificacions = db.query(Classificacio).filter(
        Classificacio.fase_id == fase_id,
        Classificacio.jornada == jornada
    ).all()
    
    if not classificacions:
        return []
    
    return classificacions

def get_classificacio_individual(db: Session, fase_id: int, jornada: int, equip_id: int):
    return db.query(Classificacio).filter(
        Classificacio.fase_id == fase_id,
        Classificacio.jornada == jornada,
        Classificacio.equip_id == equip_id
    ).first()

def delete_classificacio(db: Session, classificacio):
    db.delete(classificacio)
    db.commit()

def get_classificacio_by_id_crud(db: Session, classificacio_id: int):
    return db.query(Classificacio).filter(Classificacio.id == classificacio_id).first()
