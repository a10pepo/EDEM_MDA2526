# Aerodrome MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full-stack aerodrome management system with FastAPI backend, React frontend, PostgreSQL database, and GitHub Actions CI/CD.

**Architecture:** Monorepo with `/backend` (FastAPI + SQLAlchemy 2.0 + Alembic) and `/frontend` (Vite + React + TypeScript + shadcn/ui). PostgreSQL runs in Docker Compose locally and manually on EC2. GitHub Actions runs tests on PRs and pushes Docker images to DockerHub on merge to main. DB auto-seeds from `initial_info.py` data on first startup.

**Tech Stack:** FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL, Pydantic v2, pytest, httpx, Vite, React 18, TypeScript, TanStack Query, shadcn/ui, Tailwind CSS, Docker, Docker Compose, GitHub Actions.

---

## File Map

### Backend
- `backend/app/main.py` — FastAPI app instance, CORS, startup seed event, router registration
- `backend/app/database.py` — SQLAlchemy engine, session factory, Base, get_db dependency
- `backend/app/models.py` — ORM models: Airplane, Flight, Passenger, FlightPassenger
- `backend/app/schemas.py` — Pydantic schemas for all entities (Create + Response)
- `backend/app/seed.py` — Seed function, inserts data from initial_info.py if tables empty
- `backend/app/services/alerts.py` — Pure functions: days_until_maintenance, maintenance_alert, empty_seats_alert, fuel_alert
- `backend/app/routers/airplanes.py` — GET list, GET by id, POST create — injects computed alert fields
- `backend/app/routers/flights.py` — GET list, GET by id, POST create — injects seat/fuel alert fields
- `backend/app/routers/passengers.py` — GET list, GET by id, POST create
- `backend/tests/conftest.py` — pytest fixtures: test DB engine, rollback-per-test session, TestClient
- `backend/tests/unit/test_alerts.py` — Unit tests for pure alert functions
- `backend/tests/integration/test_airplanes.py` — API integration tests
- `backend/tests/integration/test_flights.py` — API integration tests
- `backend/tests/integration/test_passengers.py` — API integration tests
- `backend/requirements.txt` — Runtime deps
- `backend/requirements-dev.txt` — Dev/test deps
- `backend/Dockerfile` — Backend container

### Frontend
- `frontend/src/types.ts` — TypeScript interfaces for all API entities
- `frontend/src/api/client.ts` — axios base client (reads VITE_API_URL)
- `frontend/src/api/airplanes.ts` — getAirplanes, createAirplane
- `frontend/src/api/flights.ts` — getFlights, createFlight
- `frontend/src/api/passengers.ts` — getPassengers, createPassenger
- `frontend/src/components/Layout.tsx` — Nav + layout wrapper
- `frontend/src/components/AlertBadge.tsx` — Colored badge: destructive if alert=true
- `frontend/src/pages/AirplanesPage.tsx` — Table + register dialog + maintenance alert badge
- `frontend/src/pages/FlightsPage.tsx` — Table + register dialog + fuel/seats alert badges
- `frontend/src/pages/PassengersPage.tsx` — Table + register dialog
- `frontend/src/App.tsx` — React Router routes
- `frontend/src/main.tsx` — Entry point: QueryClientProvider + BrowserRouter
- `frontend/Dockerfile` — Multi-stage: node build → nginx serve
- `frontend/nginx.conf` — Serve SPA, proxy /api/ to backend

### Root
- `docker-compose.yml` — postgres + backend + frontend services
- `.github/workflows/ci.yml` — Run tests on PRs
- `.github/workflows/cd.yml` — Push images to DockerHub on merge to main

---

## Task 1: Project Scaffold

**Files:**
- Create: `docker-compose.yml`
- Create: `backend/requirements.txt`
- Create: `backend/requirements-dev.txt`
- Create: `backend/.env.example`
- Create: `backend/app/__init__.py`
- Create: `backend/app/routers/__init__.py`
- Create: `backend/app/services/__init__.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/unit/__init__.py`
- Create: `backend/tests/integration/__init__.py`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p backend/app/routers backend/app/services backend/tests/unit backend/tests/integration backend/alembic/versions
mkdir -p frontend/src/{api,components,pages}
mkdir -p .github/workflows
touch backend/app/__init__.py backend/app/routers/__init__.py backend/app/services/__init__.py
touch backend/tests/__init__.py backend/tests/unit/__init__.py backend/tests/integration/__init__.py
```

- [ ] **Step 2: Create `backend/requirements.txt`**

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.35
alembic==1.13.3
psycopg2-binary==2.9.9
pydantic==2.9.2
pydantic-settings==2.5.2
python-dotenv==1.0.1
```

- [ ] **Step 3: Create `backend/requirements-dev.txt`**

```
-r requirements.txt
pytest==8.3.3
httpx==0.27.2
```

- [ ] **Step 4: Create `backend/.env.example`**

```
DATABASE_URL=postgresql://aerodrome:aerodrome@localhost:5432/aerodrome
```

- [ ] **Step 5: Create `docker-compose.yml`**

```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: aerodrome
      POSTGRES_PASSWORD: aerodrome
      POSTGRES_DB: aerodrome
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U aerodrome"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://aerodrome:aerodrome@db:5432/aerodrome
    depends_on:
      db:
        condition: service_healthy

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

- [ ] **Step 6: Commit**

```bash
git add docker-compose.yml backend/requirements.txt backend/requirements-dev.txt backend/.env.example backend/app/__init__.py backend/app/routers/__init__.py backend/app/services/__init__.py backend/tests/__init__.py backend/tests/unit/__init__.py backend/tests/integration/__init__.py
git commit -m "chore: project scaffold with docker-compose and requirements"
```

---

## Task 2: Backend Database + Models

**Files:**
- Create: `backend/app/database.py`
- Create: `backend/app/models.py`

- [ ] **Step 1: Create `backend/app/database.py`**

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://aerodrome:aerodrome@localhost:5432/aerodrome")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 2: Create `backend/app/models.py`**

```python
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
    status: Mapped[str] = mapped_column(String, nullable=False)  # "Boarded" or "Cancelled"

    flight: Mapped["Flight"] = relationship("Flight", back_populates="passenger_associations")
    passenger: Mapped["Passenger"] = relationship(
        "Passenger", back_populates="flight_associations"
    )
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/database.py backend/app/models.py
git commit -m "feat: database engine, session, and ORM models"
```

---

## Task 3: Pydantic Schemas

**Files:**
- Create: `backend/app/schemas.py`

- [ ] **Step 1: Create `backend/app/schemas.py`**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/schemas.py
git commit -m "feat: pydantic schemas for all entities"
```

---

## Task 4: Alert Service (Pure Functions)

**Files:**
- Create: `backend/app/services/alerts.py`
- Test: `backend/tests/unit/test_alerts.py`

- [ ] **Step 1: Write failing tests in `backend/tests/unit/test_alerts.py`**

```python
from datetime import date
from app.services.alerts import days_until_maintenance, maintenance_alert, empty_seats_alert, fuel_alert


def test_days_until_maintenance_positive():
    future = date(2026, 12, 31)
    today = date(2026, 5, 16)
    assert days_until_maintenance(future, today) == 229


def test_maintenance_alert_triggered():
    future = date(2026, 6, 1)
    today = date(2026, 5, 16)
    assert maintenance_alert(future, today) is True


def test_maintenance_alert_not_triggered():
    future = date(2027, 1, 1)
    today = date(2026, 5, 16)
    assert maintenance_alert(future, today) is False


def test_empty_seats_alert_triggered():
    # 9 capacity, 7 occupied → 2 empty → 22% > 10%
    assert empty_seats_alert(capacity=9, occupied_seats=7) is True


def test_empty_seats_alert_not_triggered():
    # 9 capacity, 9 occupied → 0 empty
    assert empty_seats_alert(capacity=9, occupied_seats=9) is False


def test_fuel_alert_triggered():
    # 850 / 1000 = 85% > 10%
    assert fuel_alert(fuel_consumption=850, fuel_capacity=1000) is True


def test_fuel_alert_not_triggered():
    # 50 / 1000 = 5% < 10%
    assert fuel_alert(fuel_consumption=50, fuel_capacity=1000) is False
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && python -m pytest tests/unit/test_alerts.py -v
```

Expected: `ModuleNotFoundError` — `app.services.alerts` not found

- [ ] **Step 3: Create `backend/app/services/alerts.py`**

```python
from datetime import date


def days_until_maintenance(next_maintenance_date: date, today: date = None) -> int:
    if today is None:
        today = date.today()
    return (next_maintenance_date - today).days


def maintenance_alert(next_maintenance_date: date, today: date = None) -> bool:
    return days_until_maintenance(next_maintenance_date, today) < 100


def empty_seats_alert(capacity: int, occupied_seats: int) -> bool:
    empty = capacity - occupied_seats
    return empty > 0.1 * capacity


def fuel_alert(fuel_consumption: float, fuel_capacity: float) -> bool:
    return fuel_consumption > 0.1 * fuel_capacity
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd backend && python -m pytest tests/unit/test_alerts.py -v
```

Expected: 7 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/alerts.py backend/tests/unit/test_alerts.py
git commit -m "feat: alert business logic with unit tests"
```

---

## Task 5: Seed Data

**Files:**
- Create: `backend/app/seed.py`

- [ ] **Step 1: Create `backend/app/seed.py`**

```python
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
            fuel_consumption=850, occupied_seats=8, origin="Barcelona", destination="London",
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
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/seed.py
git commit -m "feat: database seed from initial notebook data"
```

---

## Task 6: FastAPI App + Airplane Router

**Files:**
- Create: `backend/app/main.py`
- Create: `backend/app/routers/airplanes.py`

- [ ] **Step 1: Create `backend/app/routers/airplanes.py`**

```python
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
```

- [ ] **Step 2: Create `backend/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from .models import Base
from .seed import seed_database
from .routers import airplanes, flights, passengers

app = FastAPI(title="Aerodrome API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


app.include_router(airplanes.router)
app.include_router(flights.router)
app.include_router(passengers.router)


@app.get("/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/main.py backend/app/routers/airplanes.py
git commit -m "feat: FastAPI app with airplane router"
```

---

## Task 7: Flight Router

**Files:**
- Create: `backend/app/routers/flights.py`

- [ ] **Step 1: Create `backend/app/routers/flights.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Airplane, Flight, FlightPassenger
from ..schemas import FlightCreate, FlightResponse, FlightPassengerInfo
from ..services.alerts import empty_seats_alert, fuel_alert

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
        empty_seats=airplane.capacity - flight.occupied_seats,
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
    flight_data = data.model_dump(exclude={"passengers"})
    flight = Flight(**flight_data)
    db.add(flight)
    db.flush()
    for p in data.passengers:
        db.add(FlightPassenger(flight_id=data.flight_id, passenger_id=p.passenger_id, status=p.status))
    db.commit()
    db.refresh(flight)
    return _to_response(flight, airplane)
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/routers/flights.py
git commit -m "feat: flight router with seat and fuel alerts"
```

---

## Task 8: Passenger Router

**Files:**
- Create: `backend/app/routers/passengers.py`

- [ ] **Step 1: Create `backend/app/routers/passengers.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Passenger
from ..schemas import PassengerCreate, PassengerResponse

router = APIRouter(prefix="/passengers", tags=["passengers"])


@router.get("/", response_model=list[PassengerResponse])
def list_passengers(db: Session = Depends(get_db)):
    return db.query(Passenger).all()


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
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/routers/passengers.py
git commit -m "feat: passenger router with CRUD"
```

---

## Task 9: Backend Dockerfile + Smoke Test

**Files:**
- Create: `backend/Dockerfile`

- [ ] **Step 1: Create `backend/Dockerfile`**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: Start DB and run backend locally**

```bash
# From repo root
docker compose up db -d
cd backend
cp .env.example .env
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Expected: Server starts at `http://localhost:8000`. Visit `http://localhost:8000/docs` — see Swagger UI with airplanes, flights, passengers endpoints. Visit `http://localhost:8000/airplanes/` — returns 2 seeded airplanes.

- [ ] **Step 3: Commit**

```bash
git add backend/Dockerfile
git commit -m "feat: backend Dockerfile"
```

---

## Task 10: Integration Tests

**Files:**
- Create: `backend/tests/conftest.py`
- Create: `backend/tests/integration/test_airplanes.py`
- Create: `backend/tests/integration/test_flights.py`
- Create: `backend/tests/integration/test_passengers.py`

- [ ] **Step 1: Create `backend/tests/conftest.py`**

```python
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://aerodrome:aerodrome@localhost:5432/aerodrome_test",
)

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

- [ ] **Step 2: Create `backend/tests/integration/test_airplanes.py`**

```python
def test_create_and_list_airplane(client):
    payload = {
        "plate_number": "EC-TEST1",
        "type": "Cessna 172",
        "last_maintenance_date": "2025-01-01",
        "next_maintenance_date": "2027-01-01",
        "capacity": 4,
        "owner_id": "O-99999",
        "owner_name": "Test Club",
        "hangar_id": "H-99",
        "fuel_capacity": 200.0,
    }
    response = client.post("/airplanes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["plate_number"] == "EC-TEST1"
    assert "days_until_maintenance" in data
    assert "maintenance_alert" in data

    list_response = client.get("/airplanes/")
    assert list_response.status_code == 200
    plates = [a["plate_number"] for a in list_response.json()]
    assert "EC-TEST1" in plates


def test_get_airplane_not_found(client):
    response = client.get("/airplanes/EC-NOPE")
    assert response.status_code == 404


def test_create_duplicate_airplane(client):
    payload = {
        "plate_number": "EC-DUP1",
        "type": "Test",
        "last_maintenance_date": "2025-01-01",
        "next_maintenance_date": "2027-01-01",
        "capacity": 4,
        "owner_id": "O-1",
        "owner_name": "X",
        "hangar_id": "H-1",
        "fuel_capacity": 100.0,
    }
    client.post("/airplanes/", json=payload)
    response = client.post("/airplanes/", json=payload)
    assert response.status_code == 409
```

- [ ] **Step 3: Create `backend/tests/integration/test_flights.py`**

```python
def _create_airplane(client, plate="EC-F001"):
    client.post("/airplanes/", json={
        "plate_number": plate, "type": "Test",
        "last_maintenance_date": "2025-01-01",
        "next_maintenance_date": "2027-01-01",
        "capacity": 10, "owner_id": "O-1",
        "owner_name": "X", "hangar_id": "H-1",
        "fuel_capacity": 500.0,
    })


def test_create_and_list_flight(client):
    _create_airplane(client)
    payload = {
        "flight_id": "FL-TEST-001",
        "plate_number": "EC-F001",
        "arrival_time": "2026-03-01T09:00:00",
        "departure_time": "2026-03-01T14:00:00",
        "fuel_consumption": 200.0,
        "occupied_seats": 8,
        "origin": "Madrid",
        "destination": "Paris",
        "passengers": [],
    }
    response = client.post("/flights/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["flight_id"] == "FL-TEST-001"
    assert "empty_seats" in data
    assert "empty_seats_alert" in data
    assert "fuel_alert" in data

    list_response = client.get("/flights/")
    assert list_response.status_code == 200


def test_flight_not_found(client):
    response = client.get("/flights/FL-NOPE")
    assert response.status_code == 404


def test_create_flight_missing_airplane(client):
    payload = {
        "flight_id": "FL-TEST-002",
        "plate_number": "EC-MISSING",
        "arrival_time": "2026-03-01T09:00:00",
        "departure_time": "2026-03-01T14:00:00",
        "fuel_consumption": 200.0,
        "occupied_seats": 5,
        "origin": "Madrid",
        "destination": "Paris",
        "passengers": [],
    }
    response = client.post("/flights/", json=payload)
    assert response.status_code == 404
```

- [ ] **Step 4: Create `backend/tests/integration/test_passengers.py`**

```python
def test_create_and_list_passenger(client):
    payload = {
        "passenger_id": "P-TEST-001",
        "name": "Test User",
        "national_id": "99999999Z",
        "date_of_birth": "1990-01-01",
    }
    response = client.post("/passengers/", json=payload)
    assert response.status_code == 201
    assert response.json()["passenger_id"] == "P-TEST-001"

    list_response = client.get("/passengers/")
    assert list_response.status_code == 200
    ids = [p["passenger_id"] for p in list_response.json()]
    assert "P-TEST-001" in ids


def test_passenger_not_found(client):
    response = client.get("/passengers/P-NOPE")
    assert response.status_code == 404
```

- [ ] **Step 5: Create test database and run integration tests**

```bash
# With docker-compose db running
docker exec $(docker ps -qf "ancestor=postgres:16") psql -U aerodrome -c "CREATE DATABASE aerodrome_test;"

cd backend
TEST_DATABASE_URL=postgresql://aerodrome:aerodrome@localhost:5432/aerodrome_test \
  python -m pytest tests/integration/ -v
```

Expected: All integration tests PASS

- [ ] **Step 6: Run all tests together**

```bash
cd backend
TEST_DATABASE_URL=postgresql://aerodrome:aerodrome@localhost:5432/aerodrome_test \
  python -m pytest tests/ -v
```

Expected: 7 unit + integration tests all PASS

- [ ] **Step 7: Commit**

```bash
git add backend/tests/conftest.py backend/tests/integration/
git commit -m "feat: integration tests for all API endpoints"
```

---

## Task 11: Frontend Setup

**Files:**
- Create: `frontend/` (Vite scaffold)
- Create: `frontend/src/api/client.ts`
- Create: `frontend/.env.example`

- [ ] **Step 1: Scaffold Vite + React + TypeScript project**

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
```

- [ ] **Step 2: Install runtime dependencies**

```bash
npm install @tanstack/react-query axios react-router-dom
```

- [ ] **Step 3: Install and configure Tailwind CSS**

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

- [ ] **Step 4: Update `frontend/tailwind.config.js`**

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
```

- [ ] **Step 5: Replace contents of `frontend/src/index.css`**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 6: Initialize shadcn/ui**

```bash
npx shadcn@latest init
```

When prompted: Style=Default, Base color=Slate, CSS variables=yes

- [ ] **Step 7: Add required shadcn components**

```bash
npx shadcn@latest add table button badge dialog input label
```

- [ ] **Step 8: Create `frontend/src/api/client.ts`**

```typescript
import axios from "axios";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
});

export default client;
```

- [ ] **Step 9: Create `frontend/.env.example`**

```
VITE_API_URL=http://localhost:8000
```

- [ ] **Step 10: Commit**

```bash
git add frontend/
git commit -m "feat: frontend scaffold with Vite, React, TypeScript, shadcn, Tailwind"
```

---

## Task 12: Frontend Types + API Layer

**Files:**
- Create: `frontend/src/types.ts`
- Create: `frontend/src/api/airplanes.ts`
- Create: `frontend/src/api/flights.ts`
- Create: `frontend/src/api/passengers.ts`

- [ ] **Step 1: Create `frontend/src/types.ts`**

```typescript
export interface Airplane {
  plate_number: string;
  type: string;
  last_maintenance_date: string;
  next_maintenance_date: string;
  capacity: number;
  owner_id: string;
  owner_name: string;
  hangar_id: string;
  fuel_capacity: number;
  days_until_maintenance: number;
  maintenance_alert: boolean;
}

export interface AirplaneCreate {
  plate_number: string;
  type: string;
  last_maintenance_date: string;
  next_maintenance_date: string;
  capacity: number;
  owner_id: string;
  owner_name: string;
  hangar_id: string;
  fuel_capacity: number;
}

export interface PassengerInfo {
  passenger_id: string;
  status: string;
}

export interface Flight {
  flight_id: string;
  plate_number: string;
  arrival_time: string;
  departure_time: string;
  fuel_consumption: number;
  occupied_seats: number;
  origin: string;
  destination: string;
  passengers: PassengerInfo[];
  empty_seats: number;
  empty_seats_alert: boolean;
  fuel_alert: boolean;
}

export interface FlightCreate {
  flight_id: string;
  plate_number: string;
  arrival_time: string;
  departure_time: string;
  fuel_consumption: number;
  occupied_seats: number;
  origin: string;
  destination: string;
  passengers: PassengerInfo[];
}

export interface Passenger {
  passenger_id: string;
  name: string;
  national_id: string;
  date_of_birth: string;
}

export interface PassengerCreate {
  passenger_id: string;
  name: string;
  national_id: string;
  date_of_birth: string;
}
```

- [ ] **Step 2: Create `frontend/src/api/airplanes.ts`**

```typescript
import client from "./client";
import { Airplane, AirplaneCreate } from "../types";

export const getAirplanes = () =>
  client.get<Airplane[]>("/airplanes/").then((r) => r.data);

export const createAirplane = (data: AirplaneCreate) =>
  client.post<Airplane>("/airplanes/", data).then((r) => r.data);
```

- [ ] **Step 3: Create `frontend/src/api/flights.ts`**

```typescript
import client from "./client";
import { Flight, FlightCreate } from "../types";

export const getFlights = () =>
  client.get<Flight[]>("/flights/").then((r) => r.data);

export const createFlight = (data: FlightCreate) =>
  client.post<Flight>("/flights/", data).then((r) => r.data);
```

- [ ] **Step 4: Create `frontend/src/api/passengers.ts`**

```typescript
import client from "./client";
import { Passenger, PassengerCreate } from "../types";

export const getPassengers = () =>
  client.get<Passenger[]>("/passengers/").then((r) => r.data);

export const createPassenger = (data: PassengerCreate) =>
  client.post<Passenger>("/passengers/", data).then((r) => r.data);
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/types.ts frontend/src/api/
git commit -m "feat: frontend type definitions and API client functions"
```

---

## Task 13: Frontend Layout + App Shell

**Files:**
- Create: `frontend/src/components/Layout.tsx`
- Create: `frontend/src/components/AlertBadge.tsx`
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/main.tsx`

- [ ] **Step 1: Create `frontend/src/components/AlertBadge.tsx`**

```tsx
import { Badge } from "@/components/ui/badge";

interface Props {
  alert: boolean;
  label: string;
}

export function AlertBadge({ alert, label }: Props) {
  return (
    <Badge variant={alert ? "destructive" : "secondary"}>
      {alert ? "⚠ " : ""}{label}
    </Badge>
  );
}
```

- [ ] **Step 2: Create `frontend/src/components/Layout.tsx`**

```tsx
import { Link } from "react-router-dom";

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b px-6 py-3 flex gap-6 items-center">
        <span className="font-bold text-lg">Aerodrome</span>
        <Link to="/airplanes" className="text-sm hover:underline">Airplanes</Link>
        <Link to="/flights" className="text-sm hover:underline">Flights</Link>
        <Link to="/passengers" className="text-sm hover:underline">Passengers</Link>
      </nav>
      <main className="p-6">{children}</main>
    </div>
  );
}
```

- [ ] **Step 3: Replace `frontend/src/main.tsx`**

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import "./index.css";

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);
```

- [ ] **Step 4: Replace `frontend/src/App.tsx`**

```tsx
import { Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./components/Layout";
import { AirplanesPage } from "./pages/AirplanesPage";
import { FlightsPage } from "./pages/FlightsPage";
import { PassengersPage } from "./pages/PassengersPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/airplanes" replace />} />
        <Route path="/airplanes" element={<AirplanesPage />} />
        <Route path="/flights" element={<FlightsPage />} />
        <Route path="/passengers" element={<PassengersPage />} />
      </Routes>
    </Layout>
  );
}
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/ frontend/src/App.tsx frontend/src/main.tsx
git commit -m "feat: app layout, routing, and alert badge component"
```

---

## Task 14: Airplanes Page

**Files:**
- Create: `frontend/src/pages/AirplanesPage.tsx`

- [ ] **Step 1: Create `frontend/src/pages/AirplanesPage.tsx`**

```tsx
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getAirplanes, createAirplane } from "../api/airplanes";
import { AirplaneCreate } from "../types";
import { AlertBadge } from "../components/AlertBadge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";

const emptyForm: AirplaneCreate = {
  plate_number: "", type: "", last_maintenance_date: "", next_maintenance_date: "",
  capacity: 0, owner_id: "", owner_name: "", hangar_id: "", fuel_capacity: 0,
};

export function AirplanesPage() {
  const qc = useQueryClient();
  const { data: airplanes = [], isLoading } = useQuery({
    queryKey: ["airplanes"],
    queryFn: getAirplanes,
  });
  const [form, setForm] = useState<AirplaneCreate>(emptyForm);
  const [open, setOpen] = useState(false);

  const mutation = useMutation({
    mutationFn: createAirplane,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["airplanes"] });
      setOpen(false);
      setForm(emptyForm);
    },
  });

  const set = (k: keyof AirplaneCreate) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({
      ...f,
      [k]: e.target.type === "number" ? Number(e.target.value) : e.target.value,
    }));

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Airplanes in Hangars</h1>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild><Button>Register Airplane</Button></DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>Register New Airplane</DialogTitle></DialogHeader>
            <div className="grid gap-3">
              {(["plate_number", "type", "owner_id", "owner_name", "hangar_id"] as const).map((k) => (
                <div key={k}>
                  <Label>{k}</Label>
                  <Input value={form[k] as string} onChange={set(k)} />
                </div>
              ))}
              <div>
                <Label>last_maintenance_date</Label>
                <Input type="date" value={form.last_maintenance_date} onChange={set("last_maintenance_date")} />
              </div>
              <div>
                <Label>next_maintenance_date</Label>
                <Input type="date" value={form.next_maintenance_date} onChange={set("next_maintenance_date")} />
              </div>
              <div>
                <Label>capacity</Label>
                <Input type="number" value={form.capacity} onChange={set("capacity")} />
              </div>
              <div>
                <Label>fuel_capacity</Label>
                <Input type="number" value={form.fuel_capacity} onChange={set("fuel_capacity")} />
              </div>
              <Button onClick={() => mutation.mutate(form)} disabled={mutation.isPending}>Save</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Plate</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Owner</TableHead>
            <TableHead>Hangar</TableHead>
            <TableHead>Capacity</TableHead>
            <TableHead>Next Maintenance</TableHead>
            <TableHead>Status</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {airplanes.map((a) => (
            <TableRow key={a.plate_number}>
              <TableCell>{a.plate_number}</TableCell>
              <TableCell>{a.type}</TableCell>
              <TableCell>{a.owner_name}</TableCell>
              <TableCell>{a.hangar_id}</TableCell>
              <TableCell>{a.capacity}</TableCell>
              <TableCell>{a.next_maintenance_date} ({a.days_until_maintenance}d)</TableCell>
              <TableCell>
                <AlertBadge
                  alert={a.maintenance_alert}
                  label={a.maintenance_alert ? "Maintenance Soon" : "OK"}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/pages/AirplanesPage.tsx
git commit -m "feat: airplanes page with list, register form, and maintenance alert"
```

---

## Task 15: Flights Page

**Files:**
- Create: `frontend/src/pages/FlightsPage.tsx`

- [ ] **Step 1: Create `frontend/src/pages/FlightsPage.tsx`**

```tsx
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getFlights, createFlight } from "../api/flights";
import { FlightCreate } from "../types";
import { AlertBadge } from "../components/AlertBadge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";

const emptyForm: FlightCreate = {
  flight_id: "", plate_number: "", arrival_time: "", departure_time: "",
  fuel_consumption: 0, occupied_seats: 0, origin: "", destination: "", passengers: [],
};

export function FlightsPage() {
  const qc = useQueryClient();
  const { data: flights = [], isLoading } = useQuery({
    queryKey: ["flights"],
    queryFn: getFlights,
  });
  const [form, setForm] = useState<FlightCreate>(emptyForm);
  const [open, setOpen] = useState(false);

  const mutation = useMutation({
    mutationFn: createFlight,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["flights"] });
      setOpen(false);
      setForm(emptyForm);
    },
  });

  const set = (k: keyof FlightCreate) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({
      ...f,
      [k]: e.target.type === "number" ? Number(e.target.value) : e.target.value,
    }));

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Flights</h1>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild><Button>Register Flight</Button></DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>Register New Flight</DialogTitle></DialogHeader>
            <div className="grid gap-3">
              {(["flight_id", "plate_number", "origin", "destination"] as const).map((k) => (
                <div key={k}>
                  <Label>{k}</Label>
                  <Input value={form[k] as string} onChange={set(k)} />
                </div>
              ))}
              <div>
                <Label>arrival_time</Label>
                <Input type="datetime-local" value={form.arrival_time} onChange={set("arrival_time")} />
              </div>
              <div>
                <Label>departure_time</Label>
                <Input type="datetime-local" value={form.departure_time} onChange={set("departure_time")} />
              </div>
              <div>
                <Label>fuel_consumption</Label>
                <Input type="number" value={form.fuel_consumption} onChange={set("fuel_consumption")} />
              </div>
              <div>
                <Label>occupied_seats</Label>
                <Input type="number" value={form.occupied_seats} onChange={set("occupied_seats")} />
              </div>
              <Button onClick={() => mutation.mutate(form)} disabled={mutation.isPending}>Save</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Flight ID</TableHead>
            <TableHead>Airplane</TableHead>
            <TableHead>Origin → Dest</TableHead>
            <TableHead>Arrival</TableHead>
            <TableHead>Empty Seats</TableHead>
            <TableHead>Fuel</TableHead>
            <TableHead>Occupancy</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {flights.map((f) => (
            <TableRow key={f.flight_id}>
              <TableCell>{f.flight_id}</TableCell>
              <TableCell>{f.plate_number}</TableCell>
              <TableCell>{f.origin} → {f.destination}</TableCell>
              <TableCell>{new Date(f.arrival_time).toLocaleString()}</TableCell>
              <TableCell>{f.empty_seats}</TableCell>
              <TableCell>
                <AlertBadge alert={f.fuel_alert} label={f.fuel_alert ? "High Fuel" : "OK"} />
              </TableCell>
              <TableCell>
                <AlertBadge
                  alert={f.empty_seats_alert}
                  label={f.empty_seats_alert ? "Low Occupancy" : "OK"}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/pages/FlightsPage.tsx
git commit -m "feat: flights page with list, register form, and alerts"
```

---

## Task 16: Passengers Page

**Files:**
- Create: `frontend/src/pages/PassengersPage.tsx`

- [ ] **Step 1: Create `frontend/src/pages/PassengersPage.tsx`**

```tsx
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getPassengers, createPassenger } from "../api/passengers";
import { PassengerCreate } from "../types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";

const emptyForm: PassengerCreate = {
  passenger_id: "", name: "", national_id: "", date_of_birth: "",
};

export function PassengersPage() {
  const qc = useQueryClient();
  const { data: passengers = [], isLoading } = useQuery({
    queryKey: ["passengers"],
    queryFn: getPassengers,
  });
  const [form, setForm] = useState<PassengerCreate>(emptyForm);
  const [open, setOpen] = useState(false);

  const mutation = useMutation({
    mutationFn: createPassenger,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["passengers"] });
      setOpen(false);
      setForm(emptyForm);
    },
  });

  const set = (k: keyof PassengerCreate) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Passengers</h1>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild><Button>Register Passenger</Button></DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>Register New Passenger</DialogTitle></DialogHeader>
            <div className="grid gap-3">
              {(["passenger_id", "name", "national_id"] as const).map((k) => (
                <div key={k}>
                  <Label>{k}</Label>
                  <Input value={form[k]} onChange={set(k)} />
                </div>
              ))}
              <div>
                <Label>date_of_birth</Label>
                <Input type="date" value={form.date_of_birth} onChange={set("date_of_birth")} />
              </div>
              <Button onClick={() => mutation.mutate(form)} disabled={mutation.isPending}>Save</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>National ID</TableHead>
            <TableHead>Date of Birth</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {passengers.map((p) => (
            <TableRow key={p.passenger_id}>
              <TableCell>{p.passenger_id}</TableCell>
              <TableCell>{p.name}</TableCell>
              <TableCell>{p.national_id}</TableCell>
              <TableCell>{p.date_of_birth}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

- [ ] **Step 2: Verify frontend runs**

```bash
cd frontend
cp .env.example .env
npm run dev
```

Expected: Open browser at `http://localhost:5173`. Airplanes page loads with 2 seeded planes and maintenance alert badges. Flights page shows 2 flights with fuel/occupancy badges. Passengers page shows 20 passengers. Register dialogs open and submit successfully.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/PassengersPage.tsx
git commit -m "feat: passengers page with list and register form"
```

---

## Task 17: Frontend Dockerfile

**Files:**
- Create: `frontend/Dockerfile`
- Create: `frontend/nginx.conf`

- [ ] **Step 1: Create `frontend/nginx.conf`**

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

- [ ] **Step 2: Create `frontend/Dockerfile`**

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

- [ ] **Step 3: Test full Docker Compose stack**

```bash
# From repo root
docker compose up --build
```

Expected: `http://localhost:3000` serves the frontend, `http://localhost:8000/docs` serves the API. All pages load with seeded data.

- [ ] **Step 4: Commit**

```bash
git add frontend/Dockerfile frontend/nginx.conf
git commit -m "feat: frontend Dockerfile with nginx"
```

---

## Task 18: GitHub Actions CI

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: aerodrome
          POSTGRES_PASSWORD: aerodrome
          POSTGRES_DB: aerodrome_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 5s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements-dev.txt
        working-directory: backend

      - name: Run unit tests
        run: python -m pytest tests/unit/ -v
        working-directory: backend

      - name: Run integration tests
        env:
          TEST_DATABASE_URL: postgresql://aerodrome:aerodrome@localhost:5432/aerodrome_test
        run: python -m pytest tests/integration/ -v
        working-directory: backend

  frontend-build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: npm ci
        working-directory: frontend

      - name: Build
        run: npm run build
        working-directory: frontend
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: GitHub Actions CI workflow for pull requests"
```

---

## Task 19: GitHub Actions CD

**Files:**
- Create: `.github/workflows/cd.yml`

> **Before this works:** Add these secrets in GitHub repo → Settings → Secrets → Actions:
> - `DOCKERHUB_USERNAME`: your DockerHub username
> - `DOCKERHUB_TOKEN`: DockerHub access token (create at hub.docker.com → Account Settings → Security → New Access Token)

- [ ] **Step 1: Create `.github/workflows/cd.yml`**

```yaml
name: CD

on:
  push:
    branches: [main]

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Log in to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/aerodrome-backend:latest
            ${{ secrets.DOCKERHUB_USERNAME }}/aerodrome-backend:${{ github.sha }}

      - name: Build and push frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          push: true
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/aerodrome-frontend:latest
            ${{ secrets.DOCKERHUB_USERNAME }}/aerodrome-frontend:${{ github.sha }}
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/cd.yml
git commit -m "ci: GitHub Actions CD workflow — push images to DockerHub on main"
```

---

## Self-Review

**Spec coverage:**

| Requirement | Implemented in |
|---|---|
| List airplanes in hangars | Task 6 `GET /airplanes/`, Task 14 AirplanesPage |
| List flights landed | Task 7 `GET /flights/`, Task 15 FlightsPage |
| List passengers | Task 8 `GET /passengers/`, Task 16 PassengersPage |
| Register airplane | Task 6 `POST /airplanes/`, Task 14 register dialog |
| Register flight | Task 7 `POST /flights/`, Task 15 register dialog |
| Register passenger | Task 8 `POST /passengers/`, Task 16 register dialog |
| Days until next maintenance | Task 4 `days_until_maintenance()`, Task 6 `AirplaneResponse` |
| Empty seats per flight | Task 7 `FlightResponse.empty_seats` |
| Boarding status of passengers | Task 7 `FlightResponse.passengers[].status` |
| Alert: empty seats > 10% | Task 4 `empty_seats_alert()`, Task 7, Task 15 badge |
| Alert: maintenance < 100 days | Task 4 `maintenance_alert()`, Task 6, Task 14 badge |
| Alert: fuel > 10% capacity | Task 4 `fuel_alert()`, Task 7, Task 15 badge |
| Docker Compose local | Task 1 |
| Auto-seed from initial_info.py | Task 5 + Task 6 startup event |
| CI on PRs | Task 18 |
| CD push DockerHub on main | Task 19 |
| Unit tests | Task 4 |
| Integration tests | Task 10 |

All 18 requirements covered. No placeholders. Types consistent across all tasks (`FlightPassengerInfo` used in schemas.py/flights.py/types.ts consistently, `AirplaneResponse` fields match between routers/airplanes.py and types.ts).
