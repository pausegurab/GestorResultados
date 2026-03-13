from collections import defaultdict
from http.client import HTTPException
from typing import Iterable
from sqlalchemy.orm import Session

from app.models.fases import FaseCompeticio
from app.schemas.partits import PartitSchema

from app.crud.participacio import get_temporada_by_fase_id
from app.crud.equip import get_equips_by_temporada
from app.crud.classificacio import get_classificacio_individual
from app.services.get_partits import partits_entre_equips, partits_del_grup, dos_partits_complets
from app.models.classificacions import Classificacio

def _apply_stats(cl, guanyats=0, empats=0, perduts=0,
                 gf=0, gc=0, punts=0):
    cl.partits_guanyats  += guanyats
    cl.partits_empats    += empats
    cl.partits_perduts   += perduts
    cl.gols_favor        += gf
    cl.gols_contra       += gc
    cl.punts             += punts


def ordenar_dual(bloc1, bloc2, fase_id, db,jornada=None):
    e1_id = bloc1.equip_id
    e2_id = bloc2.equip_id
    partits = partits_entre_equips(db, fase_id, e1_id, e2_id,jornada)
    temporada = get_temporada_by_fase_id(db, fase_id)
    temporada_id = temporada.temporada_id

    equips = get_equips_by_temporada(db, temporada_id)

    equips_dict  = {e.id: e.nom for e in equips}

    if not dos_partits_complets(partits, e1_id, e2_id):
        return sorted(
            [bloc1, bloc2],
            key=lambda x: (
                -x.punts,
                -(x.gols_favor - x.gols_contra),
                -x.gols_favor,
                equips_dict.get(x.equip_id, "") 
            ),
        )

    punts1 = punts2 = 0
    gf1 = gc1 = gf2 = gc2 = 0

    for p in partits:
        if p.equip_local_id == e1_id:
            gf1 += p.gols_local;  gc1 += p.gols_visitant
            gf2 += p.gols_visitant; gc2 += p.gols_local
            if p.gols_local > p.gols_visitant:   punts1 += 3
            elif p.gols_local < p.gols_visitant: punts2 += 3
            else:                                punts1 += 1; punts2 += 1
        else:
            gf1 += p.gols_visitant; gc1 += p.gols_local
            gf2 += p.gols_local;    gc2 += p.gols_visitant
            if p.gols_visitant > p.gols_local:   punts1 += 3
            elif p.gols_visitant < p.gols_local: punts2 += 3
            else:                                punts1 += 1; punts2 += 1

    diff_h2h = (gf1 - gc1) - (gf2 - gc2)

    return sorted(
        [bloc1, bloc2],
        key=lambda x: (
            -(punts1 if x == bloc1 else punts2),
            -(diff_h2h if x == bloc1 else -diff_h2h),
            -(x.gols_favor - x.gols_contra),
            -(x.gols_favor),
            equips_dict.get(x.equip_id, "") 
        ),
       
    )

def ordenar_multiple(grup, fase_id, db,jornada=None):
    ids = [e.equip_id for e in grup]
    partits = partits_del_grup(db, fase_id, ids,jornada )
    temporada = get_temporada_by_fase_id(db, fase_id)
    temporada_id = temporada.temporada_id

    equips = get_equips_by_temporada(db, temporada_id)
    equips_dict = {e.id: e.nom for e in equips}
    total_esperats = len(ids) * (len(ids) - 1)
    if len(partits) < total_esperats:
        return sorted(
            grup,
            key=lambda x: (
                -x.punts,
                -(x.gols_favor - x.gols_contra),
                -x.gols_favor,
                equips_dict.get(x.equip_id, "") 
            ),
           
        )

    stats = defaultdict(lambda: {"pts":0,"gf":0,"gc":0})
    for p in partits:
        a,b = p.equip_local_id, p.equip_visitant_id
        gl,gv = p.gols_local, p.gols_visitant
        stats[a]["gf"] += gl; stats[a]["gc"] += gv
        stats[b]["gf"] += gv; stats[b]["gc"] += gl
        if gl>gv:   stats[a]["pts"]+=3
        elif gl<gv: stats[b]["pts"]+=3
        else:       stats[a]["pts"]+=1; stats[b]["pts"]+=1

    return sorted(
        grup,
        key=lambda e: (
            -stats[e.id]["pts"],
            -stats[e.id]["gf"] - stats[e.id]["gc"],
            -(e.gols_favor - e.gols_contra),
            -e.gols_favor,
            equips_dict.get(e.equip_id, "") 
        ),
        reverse=True
    )

def ordenar_classificacio(llista, fase_id, db,jornada=None):
    llista.sort(key=lambda e: e.punts, reverse=True)
    resultat = []
    i = 0
    while i < len(llista):
        j = i
        while j < len(llista) and llista[j].punts == llista[i].punts:
            j += 1
        bloc = llista[i:j]
        if len(bloc) == 1:
            resultat.extend(bloc)
        elif len(bloc) == 2:
            resultat.extend(ordenar_dual(bloc[0], bloc[1], fase_id, db,jornada))
        else:
            print(bloc[0])
            resultat.extend(ordenar_multiple(bloc, fase_id, db,jornada))
        i = j
    return resultat


def update_classificacio(partit_updated: PartitSchema, db: Session):
    local_id      = partit_updated.equip_local_id
    visitant_id   = partit_updated.equip_visitant_id
    gols_local    = partit_updated.gols_local
    gols_visitant = partit_updated.gols_visitant
    jornada       = partit_updated.jornada
    fase_id       = partit_updated.fase_id

    cl_local = get_classificacio_individual(db, fase_id, jornada, local_id)
    cl_vis   = get_classificacio_individual(db, fase_id, jornada, visitant_id)

    if not cl_local or not cl_vis:
        raise HTTPException(status_code=404, detail="No s'ha trobat la classificació per algun equip")

    if gols_local > gols_visitant:
        delta_local = dict(guanyats=1, perduts=0, empats=0, gf=gols_local,    gc=gols_visitant, punts=3)
        delta_vis   = dict(guanyats=0, perduts=1, empats=0, gf=gols_visitant, gc=gols_local,    punts=0)
    elif gols_local < gols_visitant:
        delta_local = dict(guanyats=0, perduts=1, empats=0, gf=gols_local,    gc=gols_visitant, punts=0)
        delta_vis   = dict(guanyats=1, perduts=0, empats=0, gf=gols_visitant, gc=gols_local,    punts=3)
    else:
        delta_local = dict(guanyats=0, perduts=0, empats=1, gf=gols_local,    gc=gols_visitant, punts=1)
        delta_vis   = dict(guanyats=0, perduts=0, empats=1, gf=gols_visitant, gc=gols_local,    punts=1)

    _apply_stats(cl_local, **delta_local)
    _apply_stats(cl_vis,   **delta_vis)

    db.commit()
    db.refresh(cl_local)
    db.refresh(cl_vis)

    crear_o_actualitzar_classificacio_equips(
        db=db,
        fase_id=fase_id,
        jornada_actual=jornada,
        affected_ids=[local_id, visitant_id],
        deltas={local_id: delta_local, visitant_id: delta_vis},
    )

    return {"local": cl_local, "visitant": cl_vis}


def revertir_classificacio(partit_antic: PartitSchema, db: Session):
    fase_id = partit_antic.fase_id
    jornada = partit_antic.jornada
    local_id = partit_antic.equip_local_id
    visitant_id = partit_antic.equip_visitant_id
    gols_local = partit_antic.gols_local
    gols_visitant = partit_antic.gols_visitant

    cl_local = get_classificacio_individual(db, fase_id, jornada, local_id)
    cl_vis   = get_classificacio_individual(db, fase_id, jornada, visitant_id)

    if not cl_local or not cl_vis:
        raise HTTPException(status_code=404, detail="Classificació no trobada")

    if gols_local > gols_visitant:
        delta_local = dict(guanyats=-1, perduts=0, empats=0, gf=-gols_local,    gc=-gols_visitant, punts=-3)
        delta_vis   = dict(guanyats=0,  perduts=-1, empats=0, gf=-gols_visitant, gc=-gols_local,    punts=0)
    elif gols_local < gols_visitant:
        delta_local = dict(guanyats=0,  perduts=-1, empats=0, gf=-gols_local,    gc=-gols_visitant, punts=0)
        delta_vis   = dict(guanyats=-1, perduts=0,  empats=0, gf=-gols_visitant, gc=-gols_local,    punts=-3)
    else:
        delta_local = dict(guanyats=0, perduts=0, empats=-1, gf=-gols_local,    gc=-gols_visitant, punts=-1)
        delta_vis   = dict(guanyats=0, perduts=0, empats=-1, gf=-gols_visitant, gc=-gols_local,    punts=-1)

    _apply_stats(cl_local, **delta_local)
    _apply_stats(cl_vis,   **delta_vis)

    db.commit()

    # Propaguem el delta negatiu a totes les jornades posteriors
    crear_o_actualitzar_classificacio_equips(
        db=db,
        fase_id=fase_id,
        jornada_actual=jornada,
        affected_ids=[local_id, visitant_id],
        deltas={local_id: delta_local, visitant_id: delta_vis},
    )


def crear_o_actualitzar_classificacio_equips(
    db: Session,
    fase_id: int,
    jornada_actual: int,
    affected_ids: Iterable[int],
    deltas: dict[int, dict],
):
    if not affected_ids:
        return

    fase = db.query(FaseCompeticio).filter(FaseCompeticio.id == fase_id).first()
    if not fase:
        raise HTTPException(status_code=404, detail="Fase no trobada")

    equips          = get_equips_by_temporada(db, fase.temporada_id)
    num_equips      = len(equips)
    propera_jornada = jornada_actual + 1
    max_jornades    = (num_equips - 1) * 2

    if propera_jornada > max_jornades:
        return

    for equip_id in affected_ids:
        delta = deltas.get(equip_id)
        if not delta:
            continue

        for j in range(propera_jornada, max_jornades + 1):
            actual = db.query(Classificacio).filter_by(
                fase_id=fase_id,
                jornada=j,
                equip_id=equip_id,
            ).first()

            if actual:
                # Jornada ja existent: sumem el delta sense tocar
                # els resultats que ja hi havia en aquesta jornada
                actual.partits_guanyats += delta['guanyats']
                actual.partits_perduts  += delta['perduts']
                actual.partits_empats   += delta['empats']
                actual.gols_favor       += delta['gf']
                actual.gols_contra      += delta['gc']
                actual.punts            += delta['punts']
            else:
                # Jornada sense fila: creem-la a partir de l'anterior + delta
                anterior = db.query(Classificacio).filter_by(
                    fase_id=fase_id,
                    jornada=j - 1,
                    equip_id=equip_id,
                ).first()

                if not anterior:
                    break

                db.add(Classificacio(
                    fase_id=fase_id,
                    jornada=j,
                    equip_id=equip_id,
                    partits_guanyats=anterior.partits_guanyats + delta['guanyats'],
                    partits_perduts =anterior.partits_perduts  + delta['perduts'],
                    partits_empats  =anterior.partits_empats   + delta['empats'],
                    gols_favor      =anterior.gols_favor       + delta['gf'],
                    gols_contra     =anterior.gols_contra      + delta['gc'],
                    punts           =anterior.punts            + delta['punts'],
                ))

    db.commit()