from datetime import date, datetime
from sqlalchemy.orm import Session
from .models import Airplane, Flight, Passenger, FlightPassenger


def seed_database(db: Session) -> None:
    if db.query(Airplane).count() > 0:
        return

    airplanes = [
        Airplane(
            plate_number="EC-XYZ1", type="Cessna 208 Caravan",
            last_maintenance_date=date(2024, 4, 15), next_maintenance_date=date(2026, 4, 15),
            capacity=9, owner_id="O-12345", owner_name="Madrid Flying Club",
            hangar_id="H-01", fuel_capacity=700,
        ),
        Airplane(
            plate_number="EC-ABC2", type="Piper PA-31 Navajo",
            last_maintenance_date=date(2026, 2, 10), next_maintenance_date=date(2027, 2, 10),
            capacity=7, owner_id="O-23456", owner_name="Catalina Aviation",
            hangar_id="H-01", fuel_capacity=1000,
        ),
    ]
    db.add_all(airplanes)

    passengers = [
        Passenger(passenger_id="P-1001", name="Ana García Martínez", national_id="12345678A", date_of_birth=date(1991, 5, 15)),
        Passenger(passenger_id="P-1002", name="Carlos Rodríguez López", national_id="87654321B", date_of_birth=date(1973, 11, 30)),
        Passenger(passenger_id="P-1003", name="Elena Sánchez García", national_id="11223344C", date_of_birth=date(1988, 3, 25)),
        Passenger(passenger_id="P-1004", name="Javier Martínez Pérez", national_id="44332211D", date_of_birth=date(1995, 7, 10)),
        Passenger(passenger_id="P-1005", name="María López Rodríguez", national_id="33441122E", date_of_birth=date(1985, 9, 5)),
        Passenger(passenger_id="P-1006", name="Pedro García Sánchez", national_id="22114433F", date_of_birth=date(1979, 1, 20)),
        Passenger(passenger_id="P-1007", name="Sara Pérez Martínez", national_id="55443322G", date_of_birth=date(1999, 12, 15)),
        Passenger(passenger_id="P-1008", name="Juan Sánchez López", national_id="66554433H", date_of_birth=date(1977, 8, 25)),
        Passenger(passenger_id="P-1009", name="Lucía Martínez García", national_id="77665544I", date_of_birth=date(1990, 2, 10)),
        Passenger(passenger_id="P-1010", name="Antonio García López", national_id="88776655J", date_of_birth=date(1980, 6, 5)),
        Passenger(passenger_id="P-1011", name="Beatriz López Sánchez", national_id="99887766K", date_of_birth=date(1983, 4, 30)),
        Passenger(passenger_id="P-1012", name="Carmen Martínez Rodríguez", national_id="11001122L", date_of_birth=date(1975, 10, 15)),
        Passenger(passenger_id="P-1013", name="David Sánchez Martínez", national_id="22110033M", date_of_birth=date(1987, 3, 20)),
        Passenger(passenger_id="P-1014", name="Elena García López", national_id="33221100N", date_of_birth=date(1978, 7, 25)),
        Passenger(passenger_id="P-1015", name="Fernando López Martínez", national_id="44332211O", date_of_birth=date(1982, 1, 10)),
        Passenger(passenger_id="P-1016", name="Gloria Martínez Sánchez", national_id="55443322P", date_of_birth=date(1984, 9, 5)),
        Passenger(passenger_id="P-1017", name="Hugo Sánchez García", national_id="66554433Q", date_of_birth=date(1986, 2, 20)),
        Passenger(passenger_id="P-1018", name="Isabel García López", national_id="77665544R", date_of_birth=date(1976, 12, 15)),
        Passenger(passenger_id="P-1019", name="Javier López Martínez", national_id="88776655S", date_of_birth=date(1981, 8, 25)),
        Passenger(passenger_id="P-1020", name="Karla Martínez García", national_id="99887766T", date_of_birth=date(1989, 2, 10)),
    ]
    db.add_all(passengers)

    flights = [
        Flight(
            flight_id="FL-2025-001", plate_number="EC-XYZ1",
            arrival_time=datetime(2026, 3, 1, 9, 30), departure_time=datetime(2026, 3, 1, 14, 45),
            fuel_consumption=350, occupied_seats=7, origin="Valencia", destination="Paris",
        ),
        Flight(
            flight_id="FL-2025-002", plate_number="EC-ABC2",
            arrival_time=datetime(2026, 3, 2, 11, 15), departure_time=datetime(2026, 3, 2, 16, 30),
            fuel_consumption=850, occupied_seats=6, origin="Barcelona", destination="London",
        ),
    ]
    db.add_all(flights)
    db.flush()

    flight_passengers = [
        FlightPassenger(flight_id="FL-2025-001", passenger_id="P-1001", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-001", passenger_id="P-1002", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-001", passenger_id="P-1003", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-001", passenger_id="P-1004", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-001", passenger_id="P-1005", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-001", passenger_id="P-1006", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-002", passenger_id="P-1010", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-002", passenger_id="P-1011", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-002", passenger_id="P-1012", status="Cancelled"),
        FlightPassenger(flight_id="FL-2025-002", passenger_id="P-1013", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-002", passenger_id="P-1014", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-002", passenger_id="P-1015", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-002", passenger_id="P-1016", status="Boarded"),
        FlightPassenger(flight_id="FL-2025-002", passenger_id="P-1017", status="Cancelled"),
    ]
    db.add_all(flight_passengers)
    db.commit()
