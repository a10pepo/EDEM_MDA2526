from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional
from ..database import get_db
from ..models import Conductor

router = APIRouter()


class ConductorCreate(BaseModel):
    dni:      str
    nombre:   str
    telefono: Optional[str] = None


class ConductorRead(ConductorCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


@router.get("/conductores", response_model=list[ConductorRead])
def list_conductores(db: Session = Depends(get_db)):
    return db.query(Conductor).all()


@router.post("/conductores", response_model=ConductorRead, status_code=201)
def create_conductor(data: ConductorCreate, db: Session = Depends(get_db)):
    c = Conductor(**data.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c


@router.get("/conductores/{id}", response_model=ConductorRead)
def get_conductor(id: int, db: Session = Depends(get_db)):
    c = db.get(Conductor, id)
    if not c:
        raise HTTPException(404, "Conductor no encontrado")
    return c


@router.put("/conductores/{id}", response_model=ConductorRead)
def update_conductor(id: int, data: ConductorCreate, db: Session = Depends(get_db)):
    c = db.get(Conductor, id)
    if not c:
        raise HTTPException(404, "Conductor no encontrado")
    for k, v in data.model_dump().items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c


@router.delete("/conductores/{id}", status_code=204)
def delete_conductor(id: int, db: Session = Depends(get_db)):
    c = db.get(Conductor, id)
    if not c:
        raise HTTPException(404, "Conductor no encontrado")
    db.delete(c); db.commit()
