from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional
from ..database import get_db
from ..models import Ruta

router = APIRouter()


class RutaCreate(BaseModel):
    vehiculo_id:  int
    conductor_id: int
    origen_lat:   float
    origen_lng:   float
    destino_lat:  float
    destino_lng:  float
    actual_lat:   Optional[float] = None
    actual_lng:   Optional[float] = None
    estado:       Optional[str] = "pendiente"

    @model_validator(mode="after")
    def default_actual_to_origen(self):
        if self.actual_lat is None:
            self.actual_lat = self.origen_lat
        if self.actual_lng is None:
            self.actual_lng = self.origen_lng
        return self


class RutaUpdate(BaseModel):
    vehiculo_id:  int
    conductor_id: int
    origen_lat:   float
    origen_lng:   float
    destino_lat:  float
    destino_lng:  float
    actual_lat:   Optional[float] = None
    actual_lng:   Optional[float] = None
    estado:       Optional[str] = "pendiente"


class RutaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:           int
    vehiculo_id:  Optional[int]
    conductor_id: Optional[int]
    origen_lat:   Optional[float]
    origen_lng:   Optional[float]
    destino_lat:  Optional[float]
    destino_lng:  Optional[float]
    actual_lat:   Optional[float]
    actual_lng:   Optional[float]
    estado:       str


@router.get("/rutas", response_model=list[RutaRead])
def list_rutas(db: Session = Depends(get_db)):
    return db.query(Ruta).all()


@router.post("/rutas", response_model=RutaRead, status_code=201)
def create_ruta(data: RutaCreate, db: Session = Depends(get_db)):
    r = Ruta(**data.model_dump())
    db.add(r); db.commit(); db.refresh(r)
    return r


@router.get("/rutas/{id}", response_model=RutaRead)
def get_ruta(id: int, db: Session = Depends(get_db)):
    r = db.get(Ruta, id)
    if not r:
        raise HTTPException(404, "Ruta no encontrada")
    return r


@router.put("/rutas/{id}", response_model=RutaRead)
def update_ruta(id: int, data: RutaUpdate, db: Session = Depends(get_db)):
    r = db.get(Ruta, id)
    if not r:
        raise HTTPException(404, "Ruta no encontrada")
    for k, v in data.model_dump().items():
        setattr(r, k, v)
    db.commit(); db.refresh(r)
    return r


@router.delete("/rutas/{id}", status_code=204)
def delete_ruta(id: int, db: Session = Depends(get_db)):
    r = db.get(Ruta, id)
    if not r:
        raise HTTPException(404, "Ruta no encontrada")
    db.delete(r); db.commit()
