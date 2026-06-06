from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Vehiculo, Ruta, Pedido

router = APIRouter()


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    cutoff = date.today() + timedelta(days=30)

    vehiculos = db.query(Vehiculo).filter(Vehiculo.estado != "taller").all()
    itv = [
        {"vehiculo_id": v.id, "matricula": v.matricula, "fecha_itv": str(v.fecha_itv)}
        for v in vehiculos
        if v.fecha_itv and v.fecha_itv <= cutoff
    ]

    active_rutas = db.query(Ruta).filter(Ruta.estado == "en_ruta").all()
    sobrecarga = []
    for ruta in active_rutas:
        vehiculo = db.get(Vehiculo, ruta.vehiculo_id)
        if not vehiculo:
            continue
        pedidos = db.query(Pedido).filter(Pedido.ruta_id == ruta.id).all()
        total = sum(float(p.peso_kg) for p in pedidos)
        if total / float(vehiculo.capacidad_carga_kg) > 0.9:
            sobrecarga.append({
                "ruta_id": ruta.id,
                "matricula": vehiculo.matricula,
                "total_peso": total,
                "capacidad": float(vehiculo.capacidad_carga_kg),
            })

    return {"itv": itv, "sobrecarga": sobrecarga}
