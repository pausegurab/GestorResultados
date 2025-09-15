from fastapi import APIRouter, FastAPI
from app.api.routes import temporada, competicio, pais, equip, fase, participacio, classificacio, partit, jugador, plantilla

api_router = APIRouter()

api_router.include_router(temporada.router, prefix="/temporada", tags=["temporada"])
api_router.include_router(competicio.router, prefix="/competicio", tags=["competicio"])
api_router.include_router(pais.router, prefix="/paissos", tags=["pais"])
api_router.include_router(equip.router, prefix="/equips", tags=["equip"])   
api_router.include_router(fase.router, prefix="/fases", tags=["fase"])
api_router.include_router(participacio.router, prefix="/participacio", tags=["participacio"])
api_router.include_router(classificacio.router, prefix="/classificacio", tags=["classificacio"])
api_router.include_router(partit.router, prefix ="/partit", tags=["partits"])
api_router.include_router(jugador.router, prefix="/jugadors", tags=["jugador"])   
api_router.include_router(plantilla.router, prefix="/plantilla", tags=["plantilla"])