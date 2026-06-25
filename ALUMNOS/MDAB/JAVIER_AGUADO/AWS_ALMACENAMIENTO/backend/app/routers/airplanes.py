from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Airplane
from ..schemas import AirplaneCreate, AirplaneResponse
from ..services.alerts import days_until_maintenance, maintenance_alert

router = APIRouter(prefix="/airplanes", tags=["airplanes"])


def _to_response(airplane: Airplane) -> AirplaneResponse:
    today = date.today()
    return AirplaneResponse(
        **{c.name: getattr(airplane, c.name) for c in airplane.__table__.columns},
        days_until_maintenance=days_until_maintenance(airplane.next_maintenance_date, today),
        maintenance_alert=maintenance_alert(airplane.next_maintenance_date, today),
    )


@router.get("/", response_model=list[AirplaneResponse])
def list_airplanes(db: Session = Depends(get_db)):
    return [_to_response(a) for a in db.query(Airplane).all()]


@router.get("/{plate_number}", response_model=AirplaneResponse)
def get_airplane(plate_number: str, db: Session = Depends(get_db)):
    airplane = db.query(Airplane).filter(Airplane.plate_number == plate_number).first()
    if not airplane:
        raise HTTPException(status_code=404, detail="Airplane not found")
    return _to_response(airplane)


@router.post("/", response_model=AirplaneResponse, status_code=201)
def create_airplane(data: AirplaneCreate, db: Session = Depends(get_db)):
    if db.query(Airplane).filter(Airplane.plate_number == data.plate_number).first():
        raise HTTPException(status_code=409, detail="Airplane already exists")
    airplane = Airplane(**data.model_dump())
    db.add(airplane)
    db.commit()
    db.refresh(airplane)
    return _to_response(airplane)
