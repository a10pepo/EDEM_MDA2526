from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Airplane, Flight, FlightPassenger
from ..schemas import FlightCreate, FlightResponse, FlightPassengerInfo
from ..services.alerts import calculate_empty_seats, empty_seats_alert, fuel_alert

router = APIRouter(prefix="/flights", tags=["flights"])


def _to_response(flight: Flight, airplane: Airplane) -> FlightResponse:
    passengers = [
        FlightPassengerInfo(passenger_id=fp.passenger_id, status=fp.status)
        for fp in flight.passenger_associations
    ]
    return FlightResponse(
        flight_id=flight.flight_id,
        plate_number=flight.plate_number,
        arrival_time=flight.arrival_time,
        departure_time=flight.departure_time,
        fuel_consumption=flight.fuel_consumption,
        occupied_seats=flight.occupied_seats,
        origin=flight.origin,
        destination=flight.destination,
        passengers=passengers,
        empty_seats=calculate_empty_seats(airplane.capacity, flight.occupied_seats),
        empty_seats_alert=empty_seats_alert(airplane.capacity, flight.occupied_seats),
        fuel_alert=fuel_alert(flight.fuel_consumption, airplane.fuel_capacity),
    )


@router.get("/", response_model=list[FlightResponse])
def list_flights(db: Session = Depends(get_db)):
    flights = (
        db.query(Flight)
        .options(joinedload(Flight.passenger_associations))
        .all()
    )
    result = []
    for f in flights:
        airplane = db.query(Airplane).filter(Airplane.plate_number == f.plate_number).first()
        result.append(_to_response(f, airplane))
    return result


@router.get("/{flight_id}", response_model=FlightResponse)
def get_flight(flight_id: str, db: Session = Depends(get_db)):
    flight = (
        db.query(Flight)
        .options(joinedload(Flight.passenger_associations))
        .filter(Flight.flight_id == flight_id)
        .first()
    )
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    airplane = db.query(Airplane).filter(Airplane.plate_number == flight.plate_number).first()
    return _to_response(flight, airplane)


@router.post("/", response_model=FlightResponse, status_code=201)
def create_flight(data: FlightCreate, db: Session = Depends(get_db)):
    if db.query(Flight).filter(Flight.flight_id == data.flight_id).first():
        raise HTTPException(status_code=409, detail="Flight already exists")
    airplane = db.query(Airplane).filter(Airplane.plate_number == data.plate_number).first()
    if not airplane:
        raise HTTPException(status_code=404, detail="Airplane not found")
    if data.occupied_seats > airplane.capacity:
        raise HTTPException(status_code=400, detail="Occupied seats exceed airplane capacity")
    flight_data = data.model_dump(exclude={"passengers"})
    flight = Flight(**flight_data)
    db.add(flight)
    db.flush()
    for p in data.passengers:
        db.add(FlightPassenger(flight_id=data.flight_id, passenger_id=p.passenger_id, status=p.status))
    db.commit()
    db.refresh(flight)
    return _to_response(flight, airplane)
