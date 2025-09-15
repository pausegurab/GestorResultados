from app.models.fases import FaseCompeticio
from app.schemas.fases import FaseCreate
from sqlalchemy.orm import Session

def create_fase(db: Session, fase_in: FaseCreate) -> FaseCompeticio:
    fase = FaseCompeticio(
        nom=fase_in.nom,
        tipus=fase_in.tipus,
        temporada_id=fase_in.temporada_id,
        ordre=fase_in.ordre
    )
    db.add(fase)
    db.commit()
    db.refresh(fase)
    return fase

def get_fase_by_id(db: Session, fase_id: int) -> FaseCompeticio:
    return db.query(FaseCompeticio).filter(FaseCompeticio.id == fase_id).first()

def get_fases_by_temporada_id(db: Session, temporada_id: int) -> list[FaseCompeticio]:
    return db.query(FaseCompeticio).filter(FaseCompeticio.temporada_id == temporada_id).all()   

def get_fases(db: Session) -> list[FaseCompeticio]:
    return db.query(FaseCompeticio).all()


def get_fases_lliga_by_temporada_id(db: Session, temporada_id: int) -> list[FaseCompeticio]:
    return db.query(FaseCompeticio).filter(
        FaseCompeticio.temporada_id == temporada_id,
        FaseCompeticio.tipus == "lliga"
    ).all()