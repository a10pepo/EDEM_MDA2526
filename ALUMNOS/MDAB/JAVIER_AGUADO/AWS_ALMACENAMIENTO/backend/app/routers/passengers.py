from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Passenger
from ..schemas import PassengerCreate, PassengerResponse

router = APIRouter(prefix="/passengers", tags=["passengers"])


@router.get("/", response_model=list[PassengerResponse])
def list_passengers(db: Session = Depends(get_db)):
    return db.query(Passenger).all()

#Comment
@router.get("/{passenger_id}", response_model=PassengerResponse)
def get_passenger(passenger_id: str, db: Session = Depends(get_db)):
    passenger = db.query(Passenger).filter(Passenger.passenger_id == passenger_id).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return passenger


@router.post("/", response_model=PassengerResponse, status_code=201)
def create_passenger(data: PassengerCreate, db: Session = Depends(get_db)):
    if db.query(Passenger).filter(Passenger.passenger_id == data.passenger_id).first():
        raise HTTPException(status_code=409, detail="Passenger already exists")
    passenger = Passenger(**data.model_dump())
    db.add(passenger)
    db.commit()
    db.refresh(passenger)
    return passenger
