from app.models.equips import Equip
from app.models.participacions import Participacio
from app.schemas.equips import EquipCreate, EquipSchema
from sqlalchemy.orm import Session


def get_equips(db: Session) -> list[Equip]:
    equips = db.query(Equip).all()
    return equips

def get_equip_by_id(db: Session, equip_id: int) -> Equip | None:
    equip = db.query(Equip).filter(Equip.id == equip_id).first()
    return equip

def create_equip(db: Session, equip_in: EquipCreate) -> Equip:
    equip = Equip(
        nom=equip_in.nom,
        sigles=equip_in.sigles,
        pais_id=equip_in.pais_id,
        foto=equip_in.foto
    )
    db.add(equip)
    db.commit()
    db.refresh(equip)
    return equip

def delete_equip(db: Session, equip_id: int) -> None:
    equip = get_equip_by_id(db, equip_id)
    if equip:
        db.delete(equip)
        db.commit()
    else:
        raise ValueError("Equip not found")
    
def get_equips_by_temporada(db: Session, temporada_id: int) -> list[Equip]:
    return (
        db.query(Equip)
        .join(Participacio, Equip.id == Participacio.equip_id)
        .filter(Participacio.temporada_id == temporada_id)
        .order_by(Equip.nom)
        .all()
    )
