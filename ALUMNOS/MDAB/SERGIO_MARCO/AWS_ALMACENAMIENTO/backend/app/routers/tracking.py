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
            "origen":  {"lat": float(r.origen_lat)  if r.origen_lat  is not None else None,
                        "lng": float(r.origen_lng)  if r.origen_lng  is not None else None},
            "destino": {"lat": float(r.destino_lat) if r.destino_lat is not None else None,
                        "lng": float(r.destino_lng) if r.destino_lng is not None else None},
            "actual":  {"lat": float(r.actual_lat)  if r.actual_lat  is not None else None,
                        "lng": float(r.actual_lng)  if r.actual_lng  is not None else None},
        }
        for r in rutas
    ]
