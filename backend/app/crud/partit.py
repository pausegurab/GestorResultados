from app.models.partits import Partit
from app.schemas.partits import PartitCreate, PartitSchema, PartitUpdate    
from sqlalchemy.orm import Session

def create_partit(partit_in: PartitCreate, db: Session) -> PartitSchema:
    
    db_partit = Partit(fase_id = partit_in.fase_id, jornada = partit_in.jornada, data=partit_in.data, equip_local_id=partit_in.equip_local_id, equip_visitant_id=partit_in.equip_visitant_id,    
                       gols_local=partit_in.gols_local, gols_visitant=partit_in.gols_visitant, partit_anada_id=partit_in.partit_anada_id)
    db.add(db_partit)
    db.commit()
    db.refresh(db_partit)
    return PartitSchema(id=db_partit.id, fase_id=db_partit.fase_id, jornada=db_partit.jornada,data=db_partit.data,
                        equip_local_id=db_partit.equip_local_id, equip_visitant_id=db_partit.equip_visitant_id, gols_local=db_partit.gols_local,
                        gols_visitant=db_partit.gols_visitant, partit_anada_id=db_partit.partit_anada_id)


def get_partits(db:Session):
    partits = db.query(Partit).all()
    return partits

def get_partits_by_jornada(fase_id:int, jornada:int, db:Session):
    partits_jornada = db.query(Partit).filter(Partit.fase_id == fase_id, Partit.jornada == jornada).all()
    return partits_jornada

def get_partit_by_id(id:int, db:Session):
    partit = db.query(Partit).filter(Partit.id == id).first()
    return partit
    

def update_result(partit_result:PartitUpdate, id:int, db:Session):
    partit = get_partit_by_id(id,db)

    partit.gols_local = partit_result.gols_local
    partit.gols_visitant = partit_result.gols_visitant

    db.commit()
    db.refresh(partit)

    return partit
