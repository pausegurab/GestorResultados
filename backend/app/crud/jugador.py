from app.models.jugadors import Jugador
from app.schemas.jugadors import JugadorCreate, JugadorSchema
from sqlalchemy.orm import Session

def create_jugador(db: Session, jugador_in: JugadorCreate) -> Jugador:
    jugador = Jugador(
        nom=jugador_in.nom,
        cognom_1=jugador_in.cognom_1,
        cognom_2=jugador_in.cognom_2,
        sobrenom=jugador_in.sobrenom,
        posicio=jugador_in.posicio,
        data_naixement=jugador_in.data_naixement,
        nacionalitat=jugador_in.nacionalitat,
        url_imatge=jugador_in.url_imatge
    )
    db.add(jugador)
    db.commit()
    db.refresh(jugador)
    return jugador