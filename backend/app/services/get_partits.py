from app.models import Partit
from sqlalchemy.orm import Session

def partits_entre_equips(
    db: Session, fase_id: int, a: int, b: int, fins_jornada: int | None = None
) -> list[Partit]:
    q = db.query(Partit).filter(
        Partit.fase_id == fase_id,
        Partit.gols_local.isnot(None),
        Partit.gols_visitant.isnot(None),
        (
            ((Partit.equip_local_id == a) & (Partit.equip_visitant_id == b)) |
            ((Partit.equip_local_id == b) & (Partit.equip_visitant_id == a))
        )
    )
    if fins_jornada is not None:
        q = q.filter(Partit.jornada <= fins_jornada)

    return q.all()


def partits_del_grup(
    db: Session, fase_id: int, ids: list[int], fins_jornada: int | None = None
) -> list[Partit]:
    q = db.query(Partit).filter(
        Partit.fase_id == fase_id,
        Partit.gols_local.isnot(None),
        Partit.gols_visitant.isnot(None),
        Partit.equip_local_id.in_(ids),
        Partit.equip_visitant_id.in_(ids)
    )
    if fins_jornada is not None:
        q = q.filter(Partit.jornada <= fins_jornada)

    return q.all()


def dos_partits_complets(partits_1v1: list[Partit], eq1: int, eq2: int) -> bool:
    anada = tornada = False
    for p in partits_1v1:
        if p.equip_local_id == eq1 and p.equip_visitant_id == eq2:
            anada = True
        elif p.equip_local_id == eq2 and p.equip_visitant_id == eq1:
            tornada = True
    return anada and tornada
