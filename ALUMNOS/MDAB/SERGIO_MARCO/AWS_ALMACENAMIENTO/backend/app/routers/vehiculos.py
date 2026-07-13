from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from ..database import get_db
from ..models import Vehiculo

router = APIRouter()


class VehiculoCreate(BaseModel):
    matricula:          str
    modelo:             str
    capacidad_carga_kg: float
    fecha_itv:          date
    estado:             Optional[str] = "disponible"


class VehiculoRead(VehiculoCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


@router.get("/vehiculos", response_model=list[VehiculoRead])
def list_vehiculos(db: Session = Depends(get_db)):
    return db.query(Vehiculo).all()


@router.post("/vehiculos", response_model=VehiculoRead, status_code=201)
def create_vehiculo(data: VehiculoCreate, db: Session = Depends(get_db)):
    v = Vehiculo(**data.model_dump())
    db.add(v); db.commit(); db.refresh(v)
    return v


@router.get("/vehiculos/{id}", response_model=VehiculoRead)
def get_vehiculo(id: int, db: Session = Depends(get_db)):
    v = db.get(Vehiculo, id)
    if not v:
        raise HTTPException(404, "Vehículo no encontrado")
    return v


@router.put("/vehiculos/{id}", response_model=VehiculoRead)
def update_vehiculo(id: int, data: VehiculoCreate, db: Session = Depends(get_db)):
    v = db.get(Vehiculo, id)
    if not v:
        raise HTTPException(404, "Vehículo no encontrado")
    for k, val in data.model_dump().items():
        setattr(v, k, val)
    db.commit(); db.refresh(v)
    return v


@router.delete("/vehiculos/{id}", status_code=204)
def delete_vehiculo(id: int, db: Session = Depends(get_db)):
    v = db.get(Vehiculo, id)
    if not v:
        raise HTTPException(404, "Vehículo no encontrado")
    db.delete(v); db.commit()
