from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.jugadors import JugadorCreate, JugadorSchema
from app.core.database import get_db

from app.crud.jugador import create_jugador as create_jugador_crud
from app.models.jugadors import Jugador
router = APIRouter()

@router.post("/", response_model=JugadorSchema)
def create_jugador(jugador: JugadorCreate, db: Session = Depends(get_db)):
    jugador_creat = create_jugador_crud(db, jugador)
    if not jugador_creat:
        raise HTTPException(status_code=400, detail="Jugador could not be created")
    
    return JugadorSchema(
        id=jugador_creat.id,
        nom=jugador_creat.nom,
        cognom_1=jugador_creat.cognom_1,
        cognom_2=jugador_creat.cognom_2,
        sobrenom=jugador_creat.sobrenom,
        posicio=jugador_creat.posicio,
        data_naixement=jugador_creat.data_naixement,
        nacionalitat=jugador_creat.nacionalitat,
        url_imatge=jugador_creat.url_imatge
    )

@router.get("/", response_model=list[JugadorSchema])
def get_jugadors(db: Session = Depends(get_db)):
    jugadors = db.query(Jugador).all()
    if not jugadors:
        raise HTTPException(status_code=404, detail="No jugadors found")
    
    return jugadors

@router.delete("/{jugador_id}", response_model=JugadorSchema)
def delete_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador not found")
    
    db.delete(jugador)
    db.commit()
    
    return JugadorSchema(
        id=jugador.id,
        nom=jugador.nom,
        cognom_1=jugador.cognom_1,
        cognom_2=jugador.cognom_2,
        sobrenom=jugador.sobrenom,
        posicio=jugador.posicio,
        data_naixement=jugador.data_naixement,
        nacionalitat=jugador.nacionalitat,
        url_imatge=jugador.url_imatge
    )

@router.put("/{jugador_id}", response_model=JugadorSchema)
def update_jugador(jugador_id: int, jugador_update: JugadorCreate, db: Session = Depends(get_db)):
    jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador not found")
    
    jugador.nom = jugador_update.nom
    jugador.cognom_1 = jugador_update.cognom_1
    jugador.cognom_2 = jugador_update.cognom_2
    jugador.sobrenom = jugador_update.sobrenom
    jugador.posicio = jugador_update.posicio    
    jugador.nacionalitat = jugador_update.nacionalitat
    jugador.url_imatge = jugador_update.url_imatge
    jugador.data_naixement = jugador_update.data_naixement

       
    db.commit()
    db.refresh(jugador)
    
    return JugadorSchema(
        id=jugador.id,
        nom=jugador.nom,
        cognom_1=jugador.cognom_1,
        cognom_2=jugador.cognom_2,
        sobrenom=jugador.sobrenom,
        posicio=jugador.posicio,
        data_naixement=jugador.data_naixement,
        nacionalitat=jugador.nacionalitat,
        url_imatge=jugador.url_imatge
    )