from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Ruta

router = APIRouter()


@router.get("/routes/active")
def active_routes(db: Session = Depends(get_db)):
    rutas = db.query(Ruta).filter(Ruta.estado == "en_ruta").all()
    return [
        {
            "id":          r.id,
            "vehiculo_id": r.vehiculo_id,
            "origen":  {"lat": float(r.origen_lat),  "lng": float(r.origen_lng)},
            "destino": {"lat": float(r.destino_lat), "lng": float(r.destino_lng)},
            "actual":  {"lat": float(r.actual_lat),  "lng": float(r.actual_lng)},
        }
        for r in rutas
    ]
