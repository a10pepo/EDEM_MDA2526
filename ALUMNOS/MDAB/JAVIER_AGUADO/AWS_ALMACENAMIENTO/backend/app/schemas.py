from datetime import date, datetime
from pydantic import BaseModel


class AirplaneCreate(BaseModel):
    plate_number: str
    type: str
    last_maintenance_date: date
    next_maintenance_date: date
    capacity: int
    owner_id: str
    owner_name: str
    hangar_id: str
    fuel_capacity: float


class AirplaneResponse(AirplaneCreate):
    days_until_maintenance: int
    maintenance_alert: bool

    model_config = {"from_attributes": True}


class PassengerCreate(BaseModel):
    passenger_id: str
    name: str
    national_id: str
    date_of_birth: date


class PassengerResponse(PassengerCreate):
    model_config = {"from_attributes": True}


class FlightPassengerInfo(BaseModel):
    passenger_id: str
    status: str


class FlightCreate(BaseModel):
    flight_id: str
    plate_number: str
    arrival_time: datetime
    departure_time: datetime
    fuel_consumption: float
    occupied_seats: int
    origin: str
    destination: str
    passengers: list[FlightPassengerInfo] = []


class FlightResponse(FlightCreate):
    empty_seats: int
    empty_seats_alert: bool
    fuel_alert: bool

    model_config = {"from_attributes": True}
