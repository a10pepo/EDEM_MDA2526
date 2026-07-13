"""
Creates the four tables in RDS and seeds them with sample data.

Usage:
    pip install sqlalchemy psycopg2-binary
    DATABASE_URL=postgresql://aerodrome:Aerodrome2025!@<endpoint>:5432/aerodrome python init_db.py

Or get the URL from Terraform:
    terraform -chdir=../terraform output -raw database_url
"""

import os
import sys
from datetime import date, datetime

from sqlalchemy import create_engine, String, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: set DATABASE_URL env var before running this script.")
    sys.exit(1)


# ── Models (mirrors backend/app/models.py) ────────────────────────────────────

class Base(DeclarativeBase):
    pass


class Airplane(Base):
    __tablename__ = "airplanes"

    plate_number: Mapped[str] = mapped_column(String, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    last_maintenance_date: Mapped[date] = mapped_column(Date, nullable=False)
    next_maintenance_date: Mapped[date] = mapped_column(Date, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_id: Mapped[str] = mapped_column(String, nullable=False)
    owner_name: Mapped[str] = mapped_column(String, nullable=False)
    hangar_id: Mapped[str] = mapped_column(String, nullable=False)
    fuel_capacity: Mapped[float] = mapped_column(Float, nullable=False)

    flights: Mapped[list["Flight"]] = relationship("Flight", back_populates="airplane")


class Passenger(Base):
    __tablename__ = "passengers"

    passenger_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    national_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    flight_associations: Mapped[list["FlightPassenger"]] = relationship(
        "FlightPassenger", back_populates="passenger"
    )


class Flight(Base):
    __tablename__ = "flights"

    flight_id: Mapped[str] = mapped_column(String, primary_key=True)
    plate_number: Mapped[str] = mapped_column(
        String, ForeignKey("airplanes.plate_number"), nullable=False
    )
    arrival_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    departure_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fuel_consumption: Mapped[float] = mapped_column(Float, nullable=False)
    occupied_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    origin: Mapped[str] = mapped_column(String, nullable=False)
    destination: Mapped[str] = mapped_column(String, nullable=False)

    airplane: Mapped["Airplane"] = relationship("Airplane", back_populates="flights")
    passenger_associations: Mapped[list["FlightPassenger"]] = relationship(
        "FlightPassenger", back_populates="flight"
    )


class FlightPassenger(Base):
    __tablename__ = "flight_passengers"

    flight_id: Mapped[str] = mapped_column(
        String, ForeignKey("flights.flight_id"), primary_key=True
    )
    passenger_id: Mapped[str] = mapped_column(
        String, ForeignKey("passengers.passenger_id"), primary_key=True
    )
    status: Mapped[str] = mapped_column(String, nullable=False)

    flight: Mapped["Flight"] = relationship("Flight", back_populates="passenger_associations")
    passenger: Mapped["Passenger"] = relationship(
        "Passenger", back_populates="flight_associations"
    )


# ── Seed data (from initial_info.py) ─────────────────────────────────────────

AIRPLANES = [
    Airplane(
        plate_number="EC-XYZ1",
        type="Cessna 208 Caravan",
        last_maintenance_date=date(2024, 4, 15),
        next_maintenance_date=date(2026, 4, 15),
        capacity=9,
        owner_id="O-12345",
        owner_name="Madrid Flying Club",
        hangar_id="H-01",
        fuel_capacity=700,
    ),
    Airplane(
        plate_number="EC-ABC2",
        type="Piper PA-31 Navajo",
        last_maintenance_date=date(2026, 2, 10),
        next_maintenance_date=date(2027, 2, 10),
        capacity=7,
        owner_id="O-23456",
        owner_name="Catalina Aviation",
        hangar_id="H-01",
        fuel_capacity=1000,
    ),
]

PASSENGERS = [
    Passenger(passenger_id="P-1001", name="Ana García Martínez",       national_id="12345678A", date_of_birth=date(1991, 5, 15)),
    Passenger(passenger_id="P-1002", name="Carlos Rodríguez López",    national_id="87654321B", date_of_birth=date(1973, 11, 30)),
    Passenger(passenger_id="P-1003", name="Elena Sánchez García",      national_id="11223344C", date_of_birth=date(1988, 3, 25)),
    Passenger(passenger_id="P-1004", name="Javier Martínez Pérez",     national_id="44332211D", date_of_birth=date(1995, 7, 10)),
    Passenger(passenger_id="P-1005", name="María López Rodríguez",     national_id="33441122E", date_of_birth=date(1985, 9, 5)),
    Passenger(passenger_id="P-1006", name="Pedro García Sánchez",      national_id="22114433F", date_of_birth=date(1979, 1, 20)),
    Passenger(passenger_id="P-1007", name="Sara Pérez Martínez",       national_id="55443322G", date_of_birth=date(1999, 12, 15)),
    Passenger(passenger_id="P-1008", name="Juan Sánchez López",        national_id="66554433H", date_of_birth=date(1977, 8, 25)),
    Passenger(passenger_id="P-1009", name="Lucía Martínez García",     national_id="77665544I", date_of_birth=date(1990, 2, 10)),
    Passenger(passenger_id="P-1010", name="Antonio García López",      national_id="88776655J", date_of_birth=date(1980, 6, 5)),
    Passenger(passenger_id="P-1011", name="Beatriz López Sánchez",     national_id="99887766K", date_of_birth=date(1983, 4, 30)),
    Passenger(passenger_id="P-1012", name="Carmen Martínez Rodríguez", national_id="11001122L", date_of_birth=date(1975, 10, 15)),
    Passenger(passenger_id="P-1013", name="David Sánchez Martínez",    national_id="22110033M", date_of_birth=date(1987, 3, 20)),
    Passenger(passenger_id="P-1014", name="Elena García López",        national_id="33221100N", date_of_birth=date(1978, 7, 25)),
    Passenger(passenger_id="P-1015", name="Fernando López Martínez",   national_id="44332211O", date_of_birth=date(1982, 1, 10)),
    Passenger(passenger_id="P-1016", name="Gloria Martínez Sánchez",   national_id="55443322P", date_of_birth=date(1984, 9, 5)),
    Passenger(passenger_id="P-1017", name="Hugo Sánchez García",       national_id="66554433Q", date_of_birth=date(1986, 2, 20)),
    Passenger(passenger_id="P-1018", name="Isabel García López",       national_id="77665544R", date_of_birth=date(1976, 12, 15)),
    Passenger(passenger_id="P-1019", name="Javier López Martínez",     national_id="88776655S", date_of_birth=date(1981, 8, 25)),
    Passenger(passenger_id="P-1020", name="Karla Martínez García",     national_id="99887766T", date_of_birth=date(1989, 2, 10)),
]

FLIGHTS = [
    Flight(
        flight_id="FL-2025-001",
        plate_number="EC-XYZ1",
        arrival_time=datetime(2026, 3, 1, 9, 30),
        departure_time=datetime(2026, 3, 1, 14, 45),
        fuel_consumption=350,
        occupied_seats=7,
        origin="Valencia",
        destination="Paris",
    ),
    Flight(
        flight_id="FL-2025-002",
        plate_number="EC-ABC2",
        arrival_time=datetime(2026, 3, 2, 11, 15),
        departure_time=datetime(2026, 3, 2, 16, 30),
        fuel_consumption=850,
        occupied_seats=8,
        origin="Barcelona",
        destination="London",
    ),
]

FLIGHT_PASSENGERS = [
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


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    engine = create_engine(DATABASE_URL)

    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("  airplanes, passengers, flights, flight_passengers — OK")

    with Session(engine) as session:
        # Skip seed if already populated
        if session.query(Airplane).count() > 0:
            print("Tables already seeded. Skipping.")
            return

        print("Seeding data...")
        session.add_all(AIRPLANES)
        session.flush()
        session.add_all(PASSENGERS)
        session.flush()
        session.add_all(FLIGHTS)
        session.flush()
        session.add_all(FLIGHT_PASSENGERS)
        session.commit()

    print(f"  {len(AIRPLANES)} airplanes")
    print(f"  {len(PASSENGERS)} passengers")
    print(f"  {len(FLIGHTS)} flights")
    print(f"  {len(FLIGHT_PASSENGERS)} flight-passenger associations")
    print("\nDone. Database ready.")


if __name__ == "__main__":
    main()
