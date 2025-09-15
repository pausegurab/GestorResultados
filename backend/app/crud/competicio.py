from app.models.competicions import Competicio 
from app.schemas.competicions import CompeticioCreate, CompeticioSchema, CompeticioUpdate
from sqlalchemy.orm import Session

def create_competicio(*, db: Session, competicio_in: CompeticioCreate) -> Competicio:
    db_comptecio = Competicio(nom=competicio_in.nom,tipus=competicio_in.tipus,foto=competicio_in.foto, pais_id=competicio_in.pais_id)
    db.add(db_comptecio)
    db.commit()
    db.refresh(db_comptecio)
    return Competicio(
        id=db_comptecio.id,
        nom=db_comptecio.nom,
        tipus=db_comptecio.tipus,
        pais_id=db_comptecio.pais_id,
        foto=db_comptecio.foto
    )

def get_competicions(db: Session) -> list[Competicio]:
    competicions = db.query(Competicio).all()
    return competicions

def get_competicio_by_id(db: Session, competicio_id: int) -> Competicio:
    return db.query(Competicio).filter(Competicio.id == competicio_id).first()

def update_competicio(db: Session, competicio_in: CompeticioUpdate, competicio_id: int) -> Competicio:
    db_competicio = db.query(Competicio).filter(Competicio.id == competicio_id).first()
    if not db_competicio:
        return None
    if competicio_in.nom is not None:
        db_competicio.nom = competicio_in.nom
    if competicio_in.tipus is not None:
        db_competicio.tipus = competicio_in.tipus
    if competicio_in.foto is not None:
        db_competicio.foto = competicio_in.foto
    if competicio_in.pais_id is not None:
        db_competicio.pais_id = competicio_in.pais_id
    db.commit()
    db.refresh(db_competicio)
    return db_competicio

def delete_competicio(db: Session, competicio_id: int) -> None:
    db_competicio = db.query(Competicio).filter(Competicio.id == competicio_id).first()
    if not db_competicio:
        return None
    db.delete(db_competicio)
    db.commit()
    return {"detail": "Competicio deleted successfully"}