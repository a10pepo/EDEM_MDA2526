from datetime import date, datetime
from sqlalchemy import String, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


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
