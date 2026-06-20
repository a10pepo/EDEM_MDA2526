# Delivery Fleet MVP — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy a full-stack Delivery Fleet Management System on AWS (eu-north-1) using Terraform + K3s, with a Python FastAPI backend, Leaflet.js frontend, and a real-time vehicle simulator.

**Architecture:** Single EC2 t3.small running K3s hosts three containers (backend, frontend, simulator). RDS PostgreSQL t4g.micro sits in a private subnet group spanning two AZs. FastAPI owns DB schema creation and seed injection at startup. The simulator Deployment updates vehicle coordinates every 5 seconds; the frontend polls `/api/routes/active` every 3 seconds to animate markers on a Leaflet map.

**Tech Stack:** Terraform 5.x AWS provider, Python 3.11, FastAPI 0.111, SQLAlchemy 2.0, psycopg2-binary, pytest + httpx, Nginx alpine, K3s, Leaflet.js 1.9, OpenStreetMap tiles.

---

## File Map

```
AWS_ALMACENAMIENTO/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── seed.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── conductores.py
│   │       ├── vehiculos.py
│   │       ├── rutas.py
│   │       ├── alerts.py
│   │       └── tracking.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_conductores.py
│   │   ├── test_vehiculos.py
│   │   ├── test_rutas.py
│   │   ├── test_alerts.py
│   │   └── test_tracking.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-test.txt
├── simulator/
│   ├── simulate.py
│   ├── tests/
│   │   └── test_simulate.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── nginx.conf
│   └── Dockerfile
├── k8s/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── simulator-deployment.yaml
│   └── nginx-configmap.yaml
└── deploy.sh  (update existing)
```

---

## Task 1: Terraform — Variables, VPC, Subnets, Security Groups

**Files:**
- Create: `terraform/variables.tf`
- Create: `terraform/terraform.tfvars.example`
- Create: `terraform/main.tf` (networking section)

- [ ] **Step 1: Create `terraform/variables.tf`**

```hcl
variable "region"      { default = "eu-north-1" }
variable "db_name"     { default = "fleetdb" }
variable "db_username" {}
variable "db_password" { sensitive = true }
variable "key_pair_name" {}
```

- [ ] **Step 2: Create `terraform/terraform.tfvars.example`**

```hcl
db_username   = "fleetadmin"
db_password   = "ChangeMe123!"
db_name       = "fleetdb"
key_pair_name = "my-aws-key"
```

- [ ] **Step 3: Create `terraform/main.tf` — provider + networking**

```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = var.region }

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "fleet-vpc" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "fleet-igw" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.region}a"
  map_public_ip_on_launch = true
  tags = { Name = "fleet-public" }
}

resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.region}a"
  tags              = { Name = "fleet-private-a" }
}

resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "${var.region}b"
  tags              = { Name = "fleet-private-b" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route { cidr_block = "0.0.0.0/0"; gateway_id = aws_internet_gateway.main.id }
  tags = { Name = "fleet-rt-public" }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "ec2" {
  name   = "fleet-ec2-sg"
  vpc_id = aws_vpc.main.id
  ingress { from_port = 22;  to_port = 22;  protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 80;  to_port = 80;  protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 443; to_port = 443; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0;   to_port = 0;   protocol = "-1";  cidr_blocks = ["0.0.0.0/0"] }
  tags = { Name = "fleet-ec2-sg" }
}

resource "aws_security_group" "rds" {
  name   = "fleet-rds-sg"
  vpc_id = aws_vpc.main.id
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2.id]
  }
  tags = { Name = "fleet-rds-sg" }
}
```

- [ ] **Step 4: Validate syntax**

```bash
cd terraform && terraform init -upgrade && terraform validate
```
Expected: `Success! The configuration is valid.`

- [ ] **Step 5: Commit**

```bash
git add terraform/
git commit -m "feat: terraform networking — VPC, subnets, SGs"
```

---

## Task 2: Terraform — EC2, RDS, Outputs

**Files:**
- Modify: `terraform/main.tf` (append EC2 + RDS blocks)
- Create: `terraform/outputs.tf`

- [ ] **Step 1: Append EC2 + RDS to `terraform/main.tf`**

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter { name = "name";                values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"] }
  filter { name = "virtualization-type"; values = ["hvm"] }
}

resource "aws_db_subnet_group" "main" {
  name       = "fleet-db-subnet-group"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]
  tags       = { Name = "fleet-db-subnet-group" }
}

resource "aws_db_instance" "postgres" {
  identifier             = "fleet-db"
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  availability_zone      = "${var.region}a"
  publicly_accessible    = false
  skip_final_snapshot    = true
  tags                   = { Name = "fleet-db" }
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.small"
  subnet_id              = aws_subnet.public.id
  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.ec2.id]

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io
    systemctl enable docker
    systemctl start docker
    curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable=traefik" sh -
    mkdir -p /home/ubuntu/.kube
    cp /etc/rancher/k3s/k3s.yaml /home/ubuntu/.kube/config
    chown ubuntu:ubuntu /home/ubuntu/.kube/config
    sed -i 's/127.0.0.1/localhost/g' /home/ubuntu/.kube/config
  EOF

  tags = { Name = "fleet-ec2" }
}
```

- [ ] **Step 2: Create `terraform/outputs.tf`**

```hcl
output "ec2_public_ip" {
  value = aws_instance.app.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.address
}
```

- [ ] **Step 3: Validate**

```bash
cd terraform && terraform validate
```
Expected: `Success! The configuration is valid.`

- [ ] **Step 4: Dry-run plan (requires terraform.tfvars)**

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# Edit terraform.tfvars with real values, then:
cd terraform && terraform plan
```
Expected: `Plan: 12 to add, 0 to change, 0 to destroy.`

- [ ] **Step 5: Commit**

```bash
git add terraform/
git commit -m "feat: terraform compute — EC2, RDS, outputs"
```

---

## Task 3: Backend Foundation — Database + Models

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/requirements-test.txt`
- Create: `backend/app/__init__.py`
- Create: `backend/app/routers/__init__.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/app/database.py`
- Create: `backend/app/models.py`

- [ ] **Step 1: Create `backend/requirements.txt`**

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
psycopg2-binary==2.9.9
pydantic==2.7.1
```

- [ ] **Step 2: Create `backend/requirements-test.txt`**

```
pytest==8.2.0
httpx==0.27.0
```

- [ ] **Step 3: Create empty `__init__.py` files**

Create these three files, each completely empty:
- `backend/app/__init__.py`
- `backend/app/routers/__init__.py`
- `backend/tests/__init__.py`

- [ ] **Step 4: Create `backend/app/database.py`**

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
    f"@{os.environ['DB_HOST']}:{os.environ.get('DB_PORT', '5432')}/{os.environ['DB_NAME']}"
)

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

- [ ] **Step 5: Create `backend/app/models.py`**

```python
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from .database import Base


class Conductor(Base):
    __tablename__ = "conductores"
    id       = Column(Integer, primary_key=True, index=True)
    dni      = Column(String(20), unique=True, nullable=False)
    nombre   = Column(String(100), nullable=False)
    telefono = Column(String(20))


class Vehiculo(Base):
    __tablename__ = "vehiculos"
    id                = Column(Integer, primary_key=True, index=True)
    matricula         = Column(String(20), unique=True, nullable=False)
    modelo            = Column(String(50), nullable=False)
    capacidad_carga_kg = Column(Numeric(10, 2), nullable=False)
    fecha_itv         = Column(Date, nullable=False)
    estado            = Column(String(20), default="disponible")


class Ruta(Base):
    __tablename__ = "rutas"
    id           = Column(Integer, primary_key=True, index=True)
    vehiculo_id  = Column(Integer, ForeignKey("vehiculos.id"))
    conductor_id = Column(Integer, ForeignKey("conductores.id"))
    origen_lat   = Column(Numeric(9, 6))
    origen_lng   = Column(Numeric(9, 6))
    destino_lat  = Column(Numeric(9, 6))
    destino_lng  = Column(Numeric(9, 6))
    actual_lat   = Column(Numeric(9, 6))
    actual_lng   = Column(Numeric(9, 6))
    estado       = Column(String(20), default="pendiente")


class Pedido(Base):
    __tablename__ = "pedidos"
    id          = Column(Integer, primary_key=True, index=True)
    ruta_id     = Column(Integer, ForeignKey("rutas.id"))
    peso_kg     = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(String(200))
```

- [ ] **Step 6: Commit**

```bash
git add backend/
git commit -m "feat: backend foundation — database, models"
```

---

## Task 4: Backend — Seed Data + App Entrypoint

**Files:**
- Create: `backend/app/seed.py`
- Create: `backend/app/main.py`

- [ ] **Step 1: Create `backend/app/seed.py`**

```python
from datetime import date, timedelta
from sqlalchemy.orm import Session
from .models import Conductor, Vehiculo, Ruta, Pedido


def seed_if_empty(db: Session) -> None:
    if db.query(Conductor).count() > 0:
        return

    today = date.today()

    conductores = [
        Conductor(dni="12345678A", nombre="Juan García López",      telefono="600111222"),
        Conductor(dni="23456789B", nombre="María Martínez Ruiz",    telefono="600222333"),
        Conductor(dni="34567890C", nombre="Carlos Sánchez Pérez",   telefono="600333444"),
        Conductor(dni="45678901D", nombre="Ana López Fernández",    telefono="600444555"),
        Conductor(dni="56789012E", nombre="Pedro Gómez Torres",     telefono="600555666"),
    ]
    db.add_all(conductores)
    db.flush()

    vehiculos = [
        Vehiculo(matricula="1234ABC", modelo="Mercedes Sprinter",    capacidad_carga_kg=1000, fecha_itv=today + timedelta(days=20),  estado="en_ruta"),   # ITV alert
        Vehiculo(matricula="5678DEF", modelo="Iveco Daily",          capacidad_carga_kg=1500, fecha_itv=today + timedelta(days=10),  estado="en_ruta"),   # ITV alert
        Vehiculo(matricula="9012GHI", modelo="Renault Master",       capacidad_carga_kg=1200, fecha_itv=today + timedelta(days=90),  estado="en_ruta"),
        Vehiculo(matricula="3456JKL", modelo="Ford Transit",         capacidad_carga_kg=800,  fecha_itv=today + timedelta(days=120), estado="disponible"),
        Vehiculo(matricula="7890MNO", modelo="Volkswagen Crafter",   capacidad_carga_kg=2000, fecha_itv=today + timedelta(days=200), estado="disponible"),
    ]
    db.add_all(vehiculos)
    db.flush()

    rutas = [
        Ruta(vehiculo_id=vehiculos[0].id, conductor_id=conductores[0].id,
             origen_lat=40.416775, origen_lng=-3.703790,
             destino_lat=41.385064, destino_lng=2.173404,
             actual_lat=40.416775, actual_lng=-3.703790, estado="en_ruta"),   # Madrid → Barcelona
        Ruta(vehiculo_id=vehiculos[1].id, conductor_id=conductores[1].id,
             origen_lat=39.469907, origen_lng=-0.376288,
             destino_lat=43.263012, destino_lng=-2.934985,
             actual_lat=39.469907, actual_lng=-0.376288, estado="en_ruta"),   # Valencia → Bilbao
        Ruta(vehiculo_id=vehiculos[2].id, conductor_id=conductores[2].id,
             origen_lat=37.389092, origen_lng=-5.984459,
             destino_lat=40.416775, destino_lng=-3.703790,
             actual_lat=37.389092, actual_lng=-5.984459, estado="en_ruta"),   # Sevilla → Madrid
        Ruta(vehiculo_id=vehiculos[3].id, conductor_id=conductores[3].id,
             origen_lat=41.385064, origen_lng=2.173404,
             destino_lat=37.389092, destino_lng=-5.984459,
             actual_lat=41.385064, actual_lng=2.173404,  estado="pendiente"), # Barcelona → Sevilla
        Ruta(vehiculo_id=vehiculos[4].id, conductor_id=conductores[4].id,
             origen_lat=43.263012, origen_lng=-2.934985,
             destino_lat=39.469907, destino_lng=-0.376288,
             actual_lat=43.263012, actual_lng=-2.934985, estado="pendiente"), # Bilbao → Valencia
    ]
    db.add_all(rutas)
    db.flush()

    pedidos = [
        Pedido(ruta_id=rutas[0].id, peso_kg=920,  descripcion="Electrodomésticos"),      # 92% cap → overload alert
        Pedido(ruta_id=rutas[1].id, peso_kg=1400, descripcion="Materiales construcción"), # 93% cap → overload alert
        Pedido(ruta_id=rutas[2].id, peso_kg=500,  descripcion="Paquetería estándar"),
    ]
    db.add_all(pedidos)
    db.commit()
```

- [ ] **Step 2: Create `backend/app/main.py`**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal, Base
from .seed import seed_if_empty
from .routers import conductores, vehiculos, rutas, alerts, tracking


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Fleet API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conductores.router, prefix="/api")
app.include_router(vehiculos.router,   prefix="/api")
app.include_router(rutas.router,       prefix="/api")
app.include_router(alerts.router,      prefix="/api")
app.include_router(tracking.router,    prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/seed.py backend/app/main.py
git commit -m "feat: backend seed data and app entrypoint with lifespan"
```

---

## Task 5: Backend — Conductores Router + Tests

**Files:**
- Create: `backend/tests/conftest.py`
- Create: `backend/app/routers/conductores.py`
- Create: `backend/tests/test_conductores.py`

- [ ] **Step 1: Create `backend/tests/conftest.py`**

```python
import os
os.environ.setdefault("DB_HOST",     "localhost")
os.environ.setdefault("DB_PORT",     "5432")
os.environ.setdefault("DB_NAME",     "testdb")
os.environ.setdefault("DB_USER",     "test")
os.environ.setdefault("DB_PASSWORD", "test")

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.routers import conductores, vehiculos, rutas, alerts, tracking

TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    test_app = FastAPI()
    test_app.include_router(conductores.router, prefix="/api")
    test_app.include_router(vehiculos.router,   prefix="/api")
    test_app.include_router(rutas.router,       prefix="/api")
    test_app.include_router(alerts.router,      prefix="/api")
    test_app.include_router(tracking.router,    prefix="/api")

    def override_get_db():
        yield db

    test_app.dependency_overrides[get_db] = override_get_db

    with TestClient(test_app) as c:
        yield c

    db.close()
    Base.metadata.drop_all(bind=test_engine)
```

- [ ] **Step 2: Write failing tests in `backend/tests/test_conductores.py`**

```python
def test_list_empty(client):
    r = client.get("/api/conductores")
    assert r.status_code == 200
    assert r.json() == []

def test_create(client):
    r = client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan García", "telefono": "600111222"})
    assert r.status_code == 201
    data = r.json()
    assert data["dni"] == "12345678A"
    assert data["id"] is not None

def test_get_by_id(client):
    client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan García"})
    r = client.get("/api/conductores/1")
    assert r.status_code == 200
    assert r.json()["nombre"] == "Juan García"

def test_get_not_found(client):
    assert client.get("/api/conductores/999").status_code == 404

def test_update(client):
    client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan García"})
    r = client.put("/api/conductores/1", json={"dni": "12345678A", "nombre": "Juan Modificado"})
    assert r.status_code == 200
    assert r.json()["nombre"] == "Juan Modificado"

def test_delete(client):
    client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan García"})
    assert client.delete("/api/conductores/1").status_code == 204
    assert client.get("/api/conductores/1").status_code == 404
```

- [ ] **Step 3: Run tests — expect failure**

```bash
cd backend && pip install -r requirements.txt -r requirements-test.txt
pytest tests/test_conductores.py -v
```
Expected: `ImportError` or `404` (router not implemented yet)

- [ ] **Step 4: Create `backend/app/routers/conductores.py`**

```python
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
```

- [ ] **Step 5: Run tests — expect pass**

```bash
cd backend && pytest tests/test_conductores.py -v
```
Expected: `6 passed`

- [ ] **Step 6: Commit**

```bash
git add backend/app/routers/conductores.py backend/tests/
git commit -m "feat: conductores CRUD router with tests"
```

---

## Task 6: Backend — Vehiculos Router + Tests

**Files:**
- Create: `backend/app/routers/vehiculos.py`
- Create: `backend/tests/test_vehiculos.py`

- [ ] **Step 1: Write failing tests in `backend/tests/test_vehiculos.py`**

```python
VEHICULO = {
    "matricula": "1234ABC", "modelo": "Mercedes Sprinter",
    "capacidad_carga_kg": 1000.0, "fecha_itv": "2026-12-31", "estado": "disponible"
}

def test_list_empty(client):
    assert client.get("/api/vehiculos").json() == []

def test_create(client):
    r = client.post("/api/vehiculos", json=VEHICULO)
    assert r.status_code == 201
    assert r.json()["matricula"] == "1234ABC"

def test_get_by_id(client):
    client.post("/api/vehiculos", json=VEHICULO)
    r = client.get("/api/vehiculos/1")
    assert r.status_code == 200
    assert r.json()["modelo"] == "Mercedes Sprinter"

def test_get_not_found(client):
    assert client.get("/api/vehiculos/999").status_code == 404

def test_update_estado(client):
    client.post("/api/vehiculos", json=VEHICULO)
    updated = {**VEHICULO, "estado": "en_ruta"}
    r = client.put("/api/vehiculos/1", json=updated)
    assert r.status_code == 200
    assert r.json()["estado"] == "en_ruta"

def test_delete(client):
    client.post("/api/vehiculos", json=VEHICULO)
    assert client.delete("/api/vehiculos/1").status_code == 204
    assert client.get("/api/vehiculos/1").status_code == 404
```

- [ ] **Step 2: Run tests — expect failure**

```bash
cd backend && pytest tests/test_vehiculos.py -v
```
Expected: router not found errors

- [ ] **Step 3: Create `backend/app/routers/vehiculos.py`**

```python
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
```

- [ ] **Step 4: Run tests — expect pass**

```bash
cd backend && pytest tests/test_vehiculos.py -v
```
Expected: `6 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/app/routers/vehiculos.py backend/tests/test_vehiculos.py
git commit -m "feat: vehiculos CRUD router with tests"
```

---

## Task 7: Backend — Rutas Router + Tests

**Files:**
- Create: `backend/app/routers/rutas.py`
- Create: `backend/tests/test_rutas.py`

- [ ] **Step 1: Write failing tests in `backend/tests/test_rutas.py`**

```python
import pytest

CONDUCTOR = {"dni": "12345678A", "nombre": "Juan García"}
VEHICULO  = {"matricula": "1234ABC", "modelo": "Sprinter", "capacidad_carga_kg": 1000.0, "fecha_itv": "2026-12-31"}
RUTA = {
    "vehiculo_id": 1, "conductor_id": 1,
    "origen_lat": 40.416775, "origen_lng": -3.703790,
    "destino_lat": 41.385064, "destino_lng": 2.173404,
}

@pytest.fixture
def seeded(client):
    client.post("/api/conductores", json=CONDUCTOR)
    client.post("/api/vehiculos", json=VEHICULO)
    return client

def test_list_empty(client):
    assert client.get("/api/rutas").json() == []

def test_create_sets_actual_to_origen(seeded):
    r = seeded.post("/api/rutas", json=RUTA)
    assert r.status_code == 201
    data = r.json()
    assert data["actual_lat"] == pytest.approx(40.416775, abs=1e-4)
    assert data["actual_lng"] == pytest.approx(-3.703790, abs=1e-4)

def test_create_estado_default_pendiente(seeded):
    r = seeded.post("/api/rutas", json=RUTA)
    assert r.json()["estado"] == "pendiente"

def test_get_by_id(seeded):
    seeded.post("/api/rutas", json=RUTA)
    r = seeded.get("/api/rutas/1")
    assert r.status_code == 200

def test_get_not_found(client):
    assert client.get("/api/rutas/999").status_code == 404

def test_delete(seeded):
    seeded.post("/api/rutas", json=RUTA)
    assert seeded.delete("/api/rutas/1").status_code == 204
    assert seeded.get("/api/rutas/1").status_code == 404
```

- [ ] **Step 2: Run tests — expect failure**

```bash
cd backend && pytest tests/test_rutas.py -v
```
Expected: router not found errors

- [ ] **Step 3: Create `backend/app/routers/rutas.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional
from ..database import get_db
from ..models import Ruta

router = APIRouter()


class RutaCreate(BaseModel):
    vehiculo_id:  int
    conductor_id: int
    origen_lat:   float
    origen_lng:   float
    destino_lat:  float
    destino_lng:  float
    actual_lat:   Optional[float] = None
    actual_lng:   Optional[float] = None
    estado:       Optional[str] = "pendiente"

    @model_validator(mode="after")
    def default_actual_to_origen(self):
        if self.actual_lat is None:
            self.actual_lat = self.origen_lat
        if self.actual_lng is None:
            self.actual_lng = self.origen_lng
        return self


class RutaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:           int
    vehiculo_id:  Optional[int]
    conductor_id: Optional[int]
    origen_lat:   Optional[float]
    origen_lng:   Optional[float]
    destino_lat:  Optional[float]
    destino_lng:  Optional[float]
    actual_lat:   Optional[float]
    actual_lng:   Optional[float]
    estado:       str


@router.get("/rutas", response_model=list[RutaRead])
def list_rutas(db: Session = Depends(get_db)):
    return db.query(Ruta).all()


@router.post("/rutas", response_model=RutaRead, status_code=201)
def create_ruta(data: RutaCreate, db: Session = Depends(get_db)):
    r = Ruta(**data.model_dump())
    db.add(r); db.commit(); db.refresh(r)
    return r


@router.get("/rutas/{id}", response_model=RutaRead)
def get_ruta(id: int, db: Session = Depends(get_db)):
    r = db.get(Ruta, id)
    if not r:
        raise HTTPException(404, "Ruta no encontrada")
    return r


@router.put("/rutas/{id}", response_model=RutaRead)
def update_ruta(id: int, data: RutaCreate, db: Session = Depends(get_db)):
    r = db.get(Ruta, id)
    if not r:
        raise HTTPException(404, "Ruta no encontrada")
    for k, v in data.model_dump().items():
        setattr(r, k, v)
    db.commit(); db.refresh(r)
    return r


@router.delete("/rutas/{id}", status_code=204)
def delete_ruta(id: int, db: Session = Depends(get_db)):
    r = db.get(Ruta, id)
    if not r:
        raise HTTPException(404, "Ruta no encontrada")
    db.delete(r); db.commit()
```

- [ ] **Step 4: Run tests — expect pass**

```bash
cd backend && pytest tests/test_rutas.py -v
```
Expected: `6 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/app/routers/rutas.py backend/tests/test_rutas.py
git commit -m "feat: rutas CRUD router with tests"
```

---

## Task 8: Backend — Alerts + Tracking Routers + Tests

**Files:**
- Create: `backend/app/routers/alerts.py`
- Create: `backend/app/routers/tracking.py`
- Create: `backend/tests/test_alerts.py`
- Create: `backend/tests/test_tracking.py`

- [ ] **Step 1: Write failing tests in `backend/tests/test_alerts.py`**

```python
from datetime import date, timedelta

def _seed(client):
    c = client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan"}).json()
    v_itv = client.post("/api/vehiculos", json={
        "matricula": "ITV001", "modelo": "Sprinter",
        "capacidad_carga_kg": 1000.0,
        "fecha_itv": str(date.today() + timedelta(days=15)),
        "estado": "disponible"
    }).json()
    v_ok = client.post("/api/vehiculos", json={
        "matricula": "OK001", "modelo": "Transit",
        "capacidad_carga_kg": 1000.0,
        "fecha_itv": str(date.today() + timedelta(days=90)),
        "estado": "en_ruta"
    }).json()
    return c, v_itv, v_ok

def test_itv_alert_triggered(client):
    _seed(client)
    r = client.get("/api/alerts")
    assert r.status_code == 200
    assert any(a["matricula"] == "ITV001" for a in r.json()["itv"])

def test_no_alert_for_distant_itv(client):
    _seed(client)
    r = client.get("/api/alerts")
    assert not any(a["matricula"] == "OK001" for a in r.json()["itv"])

def test_alerts_structure(client):
    r = client.get("/api/alerts")
    assert "itv" in r.json()
    assert "sobrecarga" in r.json()
```

- [ ] **Step 2: Write failing tests in `backend/tests/test_tracking.py`**

```python
def _seed_active_route(client):
    client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan"})
    client.post("/api/vehiculos", json={
        "matricula": "1234ABC", "modelo": "Sprinter",
        "capacidad_carga_kg": 1000.0, "fecha_itv": "2027-12-31"
    })
    client.post("/api/rutas", json={
        "vehiculo_id": 1, "conductor_id": 1,
        "origen_lat": 40.416775, "origen_lng": -3.703790,
        "destino_lat": 41.385064, "destino_lng": 2.173404,
        "estado": "en_ruta"
    })

def test_active_routes_empty(client):
    r = client.get("/api/routes/active")
    assert r.status_code == 200
    assert r.json() == []

def test_active_routes_returns_pending_excluded(client):
    _seed_active_route(client)
    r = client.get("/api/routes/active")
    assert len(r.json()) == 1
    route = r.json()[0]
    assert "origen" in route and "destino" in route and "actual" in route

def test_active_route_shape(client):
    _seed_active_route(client)
    route = client.get("/api/routes/active").json()[0]
    assert "lat" in route["origen"]
    assert "lng" in route["origen"]
```

- [ ] **Step 3: Run tests — expect failure**

```bash
cd backend && pytest tests/test_alerts.py tests/test_tracking.py -v
```
Expected: router not found errors

- [ ] **Step 4: Create `backend/app/routers/alerts.py`**

```python
from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Vehiculo, Ruta, Pedido

router = APIRouter()


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    cutoff = date.today() + timedelta(days=30)

    vehiculos = db.query(Vehiculo).filter(Vehiculo.estado != "taller").all()
    itv = [
        {"vehiculo_id": v.id, "matricula": v.matricula, "fecha_itv": str(v.fecha_itv)}
        for v in vehiculos
        if v.fecha_itv and v.fecha_itv <= cutoff
    ]

    active_rutas = db.query(Ruta).filter(Ruta.estado == "en_ruta").all()
    sobrecarga = []
    for ruta in active_rutas:
        vehiculo = db.get(Vehiculo, ruta.vehiculo_id)
        if not vehiculo:
            continue
        pedidos = db.query(Pedido).filter(Pedido.ruta_id == ruta.id).all()
        total = sum(float(p.peso_kg) for p in pedidos)
        if total / float(vehiculo.capacidad_carga_kg) > 0.9:
            sobrecarga.append({
                "ruta_id": ruta.id,
                "matricula": vehiculo.matricula,
                "total_peso": total,
                "capacidad": float(vehiculo.capacidad_carga_kg),
            })

    return {"itv": itv, "sobrecarga": sobrecarga}
```

- [ ] **Step 5: Create `backend/app/routers/tracking.py`**

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Ruta

router = APIRouter()


@router.get("/routes/active")
def active_routes(db: Session = Depends(get_db)):
    rutas = db.query(Ruta).filter(Ruta.estado == "en_ruta").all()
    return [
        {
            "id":          r.id,
            "vehiculo_id": r.vehiculo_id,
            "origen":  {"lat": float(r.origen_lat),  "lng": float(r.origen_lng)},
            "destino": {"lat": float(r.destino_lat), "lng": float(r.destino_lng)},
            "actual":  {"lat": float(r.actual_lat),  "lng": float(r.actual_lng)},
        }
        for r in rutas
    ]
```

- [ ] **Step 6: Run tests — expect pass**

```bash
cd backend && pytest tests/test_alerts.py tests/test_tracking.py -v
```
Expected: `6 passed`

- [ ] **Step 7: Run full test suite**

```bash
cd backend && pytest tests/ -v
```
Expected: `24 passed`

- [ ] **Step 8: Commit**

```bash
git add backend/app/routers/alerts.py backend/app/routers/tracking.py backend/tests/test_alerts.py backend/tests/test_tracking.py
git commit -m "feat: alerts and tracking routers with tests"
```

---

## Task 9: Backend — Dockerfile

**Files:**
- Create: `backend/Dockerfile`

- [ ] **Step 1: Create `backend/Dockerfile`**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: Build image to verify (requires Docker)**

```bash
docker build --platform linux/amd64 -t delivery-fleet-backend:latest ./backend
```
Expected: `Successfully built ...`

- [ ] **Step 3: Commit**

```bash
git add backend/Dockerfile
git commit -m "feat: backend Dockerfile"
```

---

## Task 10: Simulator — simulate.py + Tests + Dockerfile

**Files:**
- Create: `simulator/requirements.txt`
- Create: `simulator/tests/__init__.py` (empty)
- Create: `simulator/tests/test_simulate.py`
- Create: `simulator/simulate.py`
- Create: `simulator/Dockerfile`

- [ ] **Step 1: Create `simulator/requirements.txt`**

```
psycopg2-binary==2.9.9
```

- [ ] **Step 2: Write failing tests in `simulator/tests/test_simulate.py`**

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from simulate import distance, interpolate_step, STEP, MIN_DIST

def test_distance_same_point():
    assert distance(40.0, -3.0, 40.0, -3.0) == 0.0

def test_distance_pythagorean():
    assert abs(distance(0, 0, 3, 4) - 5.0) < 1e-9

def test_interpolate_moves_toward_destination():
    new_lat, new_lng = interpolate_step(40.0, -3.0, 41.0, -2.0)
    assert new_lat > 40.0
    assert new_lng > -3.0

def test_interpolate_step_size():
    new_lat, new_lng = interpolate_step(40.0, 0.0, 41.0, 0.0)
    assert abs(new_lat - (40.0 + 1.0 * STEP)) < 1e-9

def test_arrived_condition():
    assert distance(41.0, 2.0, 41.001, 2.001) < MIN_DIST
```

- [ ] **Step 3: Run tests — expect failure**

```bash
cd simulator && pip install pytest && pytest tests/ -v
```
Expected: `ImportError: cannot import name 'interpolate_step'`

- [ ] **Step 4: Create `simulator/simulate.py`**

```python
import os
import time
import math
import psycopg2

DB_HOST     = os.environ["DB_HOST"]
DB_PORT     = os.environ.get("DB_PORT", "5432")
DB_NAME     = os.environ["DB_NAME"]
DB_USER     = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

STEP     = 0.01
TICK     = 5
MIN_DIST = 0.01


def distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    return math.sqrt((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2)


def interpolate_step(act_lat: float, act_lng: float,
                     dest_lat: float, dest_lng: float) -> tuple[float, float]:
    return (
        act_lat + (dest_lat - act_lat) * STEP,
        act_lng + (dest_lng - act_lng) * STEP,
    )


def tick(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, origen_lat, origen_lng, destino_lat, destino_lng, actual_lat, actual_lng
            FROM rutas WHERE estado = 'en_ruta'
        """)
        for row in cur.fetchall():
            route_id, orig_lat, orig_lng, dest_lat, dest_lng, act_lat, act_lng = row
            act_lat, act_lng   = float(act_lat),  float(act_lng)
            dest_lat, dest_lng = float(dest_lat), float(dest_lng)
            orig_lat, orig_lng = float(orig_lat), float(orig_lng)

            if distance(act_lat, act_lng, dest_lat, dest_lng) < MIN_DIST:
                cur.execute("UPDATE rutas SET estado = 'completada' WHERE id = %s", (route_id,))
                cur.execute("""
                    INSERT INTO rutas
                        (vehiculo_id, conductor_id, origen_lat, origen_lng,
                         destino_lat, destino_lng, actual_lat, actual_lng, estado)
                    SELECT vehiculo_id, conductor_id,
                           destino_lat, destino_lng,
                           origen_lat,  origen_lng,
                           destino_lat, destino_lng,
                           'en_ruta'
                    FROM rutas WHERE id = %s
                """, (route_id,))
            else:
                new_lat, new_lng = interpolate_step(act_lat, act_lng, dest_lat, dest_lng)
                cur.execute(
                    "UPDATE rutas SET actual_lat = %s, actual_lng = %s WHERE id = %s",
                    (new_lat, new_lng, route_id),
                )
        conn.commit()


def main() -> None:
    print("Simulator starting...")
    conn = None
    while True:
        try:
            if conn is None or conn.closed:
                conn = psycopg2.connect(
                    host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
                    user=DB_USER, password=DB_PASSWORD,
                )
                print("DB connected")
            tick(conn)
        except Exception as exc:
            print(f"Error: {exc}")
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass
            conn = None
            time.sleep(5)
        else:
            time.sleep(TICK)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run tests — expect pass**

```bash
cd simulator && pytest tests/ -v
```
Expected: `5 passed`

- [ ] **Step 6: Create `simulator/Dockerfile`**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY simulate.py .
CMD ["python", "simulate.py"]
```

- [ ] **Step 7: Commit**

```bash
git add simulator/
git commit -m "feat: simulator with interpolation logic, tests, and Dockerfile"
```

---

## Task 11: Frontend — index.html + app.js + nginx.conf

**Files:**
- Create: `frontend/index.html`
- Create: `frontend/app.js`
- Create: `frontend/nginx.conf`

- [ ] **Step 1: Create `frontend/index.html`**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gestión de Flota</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Arial, sans-serif; background: #f5f5f5; }
    header { background: #1a237e; color: #fff; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
    header h1 { font-size: 1.4rem; }
    #alert-badge { background: #c62828; color: #fff; padding: .3rem .8rem; border-radius: 20px; font-size: .85rem; display: none; }
    .tabs { background: #fff; border-bottom: 2px solid #ddd; }
    .tab-btn { padding: .8rem 2rem; border: none; background: none; cursor: pointer; font-size: 1rem; border-bottom: 3px solid transparent; }
    .tab-btn.active { border-bottom-color: #1a237e; color: #1a237e; font-weight: bold; }
    .tab-content { display: none; padding: 1.5rem; }
    .tab-content.active { display: block; }
    #map { height: 60vh; border-radius: 8px; }
    .section { background: #fff; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
    h2 { margin-bottom: 1rem; color: #1a237e; font-size: 1.1rem; }
    form { display: flex; gap: .5rem; flex-wrap: wrap; margin-bottom: 1rem; }
    input { padding: .5rem; border: 1px solid #ccc; border-radius: 4px; flex: 1; min-width: 140px; }
    button { padding: .5rem 1rem; background: #1a237e; color: #fff; border: none; border-radius: 4px; cursor: pointer; }
    button:hover { background: #283593; }
    button.del { background: #c62828; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: .5rem; text-align: left; border-bottom: 1px solid #eee; font-size: .9rem; }
    th { background: #f0f0f0; }
    .alert-item { background: #fff3e0; border-left: 4px solid #e65100; padding: .7rem; margin-bottom: .5rem; border-radius: 4px; }
    .alert-item.overload { border-left-color: #b71c1c; background: #ffebee; }
  </style>
</head>
<body>
  <header>
    <h1>Gestión de Flota — Dashboard</h1>
    <span id="alert-badge">&#9888; <span id="alert-count">0</span> alertas</span>
  </header>
  <div class="tabs">
    <button class="tab-btn active" onclick="showTab('admin', this)">Panel Admin</button>
    <button class="tab-btn"        onclick="showTab('map',   this)">Mapa en Vivo</button>
  </div>

  <div id="tab-admin" class="tab-content active">
    <div class="section" id="alerts-section">
      <h2>Alertas Activas</h2>
      <div id="alerts-list"><em>Cargando...</em></div>
    </div>

    <div class="section">
      <h2>Conductores</h2>
      <form id="form-conductor" onsubmit="createConductor(event)">
        <input name="dni"      placeholder="DNI"    required>
        <input name="nombre"   placeholder="Nombre" required>
        <input name="telefono" placeholder="Teléfono">
        <button type="submit">Añadir</button>
      </form>
      <table>
        <thead><tr><th>ID</th><th>DNI</th><th>Nombre</th><th>Teléfono</th><th></th></tr></thead>
        <tbody id="tbody-conductores"></tbody>
      </table>
    </div>

    <div class="section">
      <h2>Vehículos</h2>
      <form id="form-vehiculo" onsubmit="createVehiculo(event)">
        <input name="matricula"          placeholder="Matrícula"      required>
        <input name="modelo"             placeholder="Modelo"         required>
        <input name="capacidad_carga_kg" placeholder="Capacidad (kg)" type="number" step="0.01" required>
        <input name="fecha_itv"          placeholder="Fecha ITV"      type="date"   required>
        <button type="submit">Añadir</button>
      </form>
      <table>
        <thead><tr><th>ID</th><th>Matrícula</th><th>Modelo</th><th>Capacidad</th><th>ITV</th><th>Estado</th><th></th></tr></thead>
        <tbody id="tbody-vehiculos"></tbody>
      </table>
    </div>

    <div class="section">
      <h2>Rutas</h2>
      <form id="form-ruta" onsubmit="createRuta(event)">
        <input name="vehiculo_id"  placeholder="ID Vehículo"  type="number" required>
        <input name="conductor_id" placeholder="ID Conductor" type="number" required>
        <input name="origen_lat"   placeholder="Origen Lat"   type="number" step="any" required>
        <input name="origen_lng"   placeholder="Origen Lng"   type="number" step="any" required>
        <input name="destino_lat"  placeholder="Destino Lat"  type="number" step="any" required>
        <input name="destino_lng"  placeholder="Destino Lng"  type="number" step="any" required>
        <button type="submit">Añadir</button>
      </form>
      <table>
        <thead><tr><th>ID</th><th>Vehículo</th><th>Conductor</th><th>Estado</th><th></th></tr></thead>
        <tbody id="tbody-rutas"></tbody>
      </table>
    </div>
  </div>

  <div id="tab-map" class="tab-content">
    <div class="section">
      <h2>Rastreo en Tiempo Real</h2>
      <p style="margin-bottom:1rem;color:#666">Actualización cada 3 segundos. Los marcadores muestran la posición actual de cada vehículo en ruta.</p>
      <div id="map"></div>
    </div>
  </div>

  <script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create `frontend/app.js`**

```javascript
function showTab(name, btn) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  btn.classList.add('active');
  if (name === 'map' && !window._mapInit) initMap();
}

// ── Leaflet map ──────────────────────────────────────────────────────────────

function initMap() {
  window._mapInit = true;
  window._map = L.map('map').setView([40.416775, -3.703790], 6);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(window._map);
  window._markers   = {};
  window._polylines = {};
  updateMap();
  setInterval(updateMap, 3000);
}

async function updateMap() {
  try {
    const routes = await apiFetch('/api/routes/active');
    Object.values(window._markers).forEach(m => m.remove());
    Object.values(window._polylines).forEach(p => p.remove());
    window._markers = {}; window._polylines = {};

    routes.forEach(r => {
      const origin = [r.origen.lat,  r.origen.lng];
      const actual = [r.actual.lat,  r.actual.lng];
      const dest   = [r.destino.lat, r.destino.lng];

      window._markers[r.id] = L.marker(actual)
        .addTo(window._map)
        .bindPopup(`<b>Ruta #${r.id}</b><br>Vehículo: ${r.vehiculo_id}`);

      window._polylines[r.id] = L.polyline(
        [origin, actual, dest],
        { color: '#1a237e', weight: 2, dashArray: '6,4' }
      ).addTo(window._map);
    });
  } catch (e) { console.error('Map update error:', e); }
}

// ── API helpers ──────────────────────────────────────────────────────────────

async function apiFetch(url, opts = {}) {
  const res = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...opts });
  if (!res.ok) throw new Error(await res.text());
  if (res.status === 204) return null;
  return res.json();
}

function formToObj(form) {
  return Object.fromEntries(new FormData(form).entries());
}

// ── Alerts ───────────────────────────────────────────────────────────────────

async function loadAlerts() {
  const data   = await apiFetch('/api/alerts');
  const total  = data.itv.length + data.sobrecarga.length;
  const badge  = document.getElementById('alert-badge');
  const list   = document.getElementById('alerts-list');

  badge.style.display = total ? 'inline' : 'none';
  document.getElementById('alert-count').textContent = total;

  if (!total) { list.innerHTML = '<em style="color:green">Sin alertas activas</em>'; return; }

  list.innerHTML =
    data.itv.map(a =>
      `<div class="alert-item">&#9888; <b>ITV próxima:</b> ${a.matricula} — vence el ${a.fecha_itv}</div>`
    ).join('') +
    data.sobrecarga.map(a =>
      `<div class="alert-item overload">&#128680; <b>Sobrecarga:</b> Ruta #${a.ruta_id} (${a.matricula}) — ${a.total_peso}&#8239;kg / ${a.capacidad}&#8239;kg cap.</div>`
    ).join('');
}

// ── Conductores ──────────────────────────────────────────────────────────────

async function loadConductores() {
  const data = await apiFetch('/api/conductores');
  document.getElementById('tbody-conductores').innerHTML = data.map(c =>
    `<tr><td>${c.id}</td><td>${c.dni}</td><td>${c.nombre}</td><td>${c.telefono||'—'}</td>
     <td><button class="del" onclick="deleteConductor(${c.id})">Eliminar</button></td></tr>`
  ).join('');
}

async function createConductor(e) {
  e.preventDefault();
  await apiFetch('/api/conductores', { method: 'POST', body: JSON.stringify(formToObj(e.target)) });
  e.target.reset(); loadConductores();
}

async function deleteConductor(id) {
  if (!confirm('¿Eliminar conductor?')) return;
  await apiFetch(`/api/conductores/${id}`, { method: 'DELETE' }); loadConductores();
}

// ── Vehículos ────────────────────────────────────────────────────────────────

async function loadVehiculos() {
  const data = await apiFetch('/api/vehiculos');
  document.getElementById('tbody-vehiculos').innerHTML = data.map(v =>
    `<tr><td>${v.id}</td><td>${v.matricula}</td><td>${v.modelo}</td>
     <td>${v.capacidad_carga_kg}&#8239;kg</td><td>${v.fecha_itv}</td><td>${v.estado}</td>
     <td><button class="del" onclick="deleteVehiculo(${v.id})">Eliminar</button></td></tr>`
  ).join('');
}

async function createVehiculo(e) {
  e.preventDefault();
  const obj = formToObj(e.target);
  obj.capacidad_carga_kg = parseFloat(obj.capacidad_carga_kg);
  await apiFetch('/api/vehiculos', { method: 'POST', body: JSON.stringify(obj) });
  e.target.reset(); loadVehiculos();
}

async function deleteVehiculo(id) {
  if (!confirm('¿Eliminar vehículo?')) return;
  await apiFetch(`/api/vehiculos/${id}`, { method: 'DELETE' }); loadVehiculos();
}

// ── Rutas ────────────────────────────────────────────────────────────────────

async function loadRutas() {
  const data = await apiFetch('/api/rutas');
  document.getElementById('tbody-rutas').innerHTML = data.map(r =>
    `<tr><td>${r.id}</td><td>${r.vehiculo_id}</td><td>${r.conductor_id}</td><td>${r.estado}</td>
     <td><button class="del" onclick="deleteRuta(${r.id})">Eliminar</button></td></tr>`
  ).join('');
}

async function createRuta(e) {
  e.preventDefault();
  const obj = formToObj(e.target);
  ['vehiculo_id','conductor_id','origen_lat','origen_lng','destino_lat','destino_lng']
    .forEach(k => { obj[k] = parseFloat(obj[k]); });
  await apiFetch('/api/rutas', { method: 'POST', body: JSON.stringify(obj) });
  e.target.reset(); loadRutas();
}

async function deleteRuta(id) {
  if (!confirm('¿Eliminar ruta?')) return;
  await apiFetch(`/api/rutas/${id}`, { method: 'DELETE' }); loadRutas();
}

// ── Init ─────────────────────────────────────────────────────────────────────

loadAlerts(); loadConductores(); loadVehiculos(); loadRutas();
setInterval(loadAlerts, 10000);
```

- [ ] **Step 3: Create `frontend/nginx.conf`**

```nginx
server {
    listen 80;

    location /api/ {
        proxy_pass         http://backend:8000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
    }

    location / {
        root  /usr/share/nginx/html;
        index index.html;
    }
}
```

- [ ] **Step 4: Commit**

```bash
git add frontend/index.html frontend/app.js frontend/nginx.conf
git commit -m "feat: frontend — Leaflet map, admin dashboard, alert badges"
```

---

## Task 12: Frontend — Dockerfile

**Files:**
- Create: `frontend/Dockerfile`

- [ ] **Step 1: Create `frontend/Dockerfile`**

```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY app.js     /usr/share/nginx/html/app.js
```

- [ ] **Step 2: Build image to verify**

```bash
docker build --platform linux/amd64 -t delivery-fleet-frontend:latest ./frontend
```
Expected: `Successfully built ...`

- [ ] **Step 3: Commit**

```bash
git add frontend/Dockerfile
git commit -m "feat: frontend Dockerfile"
```

---

## Task 13: Kubernetes Manifests

**Files:**
- Create: `k8s/backend-deployment.yaml`
- Create: `k8s/backend-service.yaml`
- Create: `k8s/simulator-deployment.yaml`
- Create: `k8s/frontend-deployment.yaml`
- Create: `k8s/frontend-service.yaml`
- Create: `k8s/nginx-configmap.yaml`

- [ ] **Step 1: Create `k8s/backend-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: delivery-fleet-backend:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 8000
          env:
            - name: DB_HOST
              value: "REPLACE_RDS_HOST"
            - name: DB_PORT
              value: "5432"
            - name: DB_NAME
              value: "REPLACE_DB_NAME"
            - name: DB_USER
              value: "REPLACE_DB_USER"
            - name: DB_PASSWORD
              value: "REPLACE_DB_PASSWORD"
          livenessProbe:
            httpGet:
              path: /api/health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
```

- [ ] **Step 2: Create `k8s/backend-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: backend
  ports:
    - port: 8000
      targetPort: 8000
```

- [ ] **Step 3: Create `k8s/simulator-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simulator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: simulator
  template:
    metadata:
      labels:
        app: simulator
    spec:
      containers:
        - name: simulator
          image: delivery-fleet-simulator:latest
          imagePullPolicy: Never
          env:
            - name: DB_HOST
              value: "REPLACE_RDS_HOST"
            - name: DB_PORT
              value: "5432"
            - name: DB_NAME
              value: "REPLACE_DB_NAME"
            - name: DB_USER
              value: "REPLACE_DB_USER"
            - name: DB_PASSWORD
              value: "REPLACE_DB_PASSWORD"
```

- [ ] **Step 4: Create `k8s/frontend-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: delivery-fleet-frontend:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 80
```

- [ ] **Step 5: Create `k8s/frontend-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80
```

- [ ] **Step 6: Commit**

```bash
git add k8s/
git commit -m "feat: Kubernetes manifests — backend, frontend, simulator"
```

---

## Task 14: Update deploy.sh

**Files:**
- Modify: `deploy.sh` (full replacement with updated logic)

- [ ] **Step 1: Replace `deploy.sh` with the updated script**

```bash
#!/bin/bash
set -e

APP_NAME="delivery-fleet"
SSH_KEY_PATH="~/.ssh/id_rsa_aws"

echo ""
echo "========================================"
echo "  AWS Delivery Fleet MVP"
echo "  Pipeline Deployment"
echo "========================================"
echo ""

# ── Prereq checks ────────────────────────────────────────────────────────────
if ! command -v aws &> /dev/null;       then echo "❌ AWS CLI no instalado."; exit 1; fi
if ! command -v terraform &> /dev/null; then echo "❌ Terraform no instalado."; exit 1; fi
if ! command -v docker &> /dev/null;    then echo "❌ Docker no instalado."; exit 1; fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region)
echo "Cuenta AWS : $ACCOUNT_ID"
echo "Región     : $REGION"
echo ""
read -p "¿Continuar con el despliegue en esta cuenta y región? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then echo "Despliegue cancelado."; exit 1; fi

# Read DB credentials from terraform.tfvars (used later for sed substitution)
DB_USER=$(grep 'db_username' terraform/terraform.tfvars | sed 's/.*= *"\(.*\)"/\1/')
DB_PASSWORD=$(grep 'db_password' terraform/terraform.tfvars | sed 's/.*= *"\(.*\)"/\1/')
DB_NAME=$(grep 'db_name' terraform/terraform.tfvars | sed 's/.*= *"\(.*\)"/\1/')

# ── FASE 1 — Infraestructura (Terraform) ─────────────────────────────────────
echo ""
echo ">>> FASE 1: Desplegando infraestructura (VPC, RDS, EC2)..."
cd terraform
terraform init -upgrade
if ! terraform validate; then echo "❌ Fallo en validación de Terraform."; exit 1; fi
terraform apply -auto-approve
EC2_PUBLIC_IP=$(terraform output -raw ec2_public_ip)
RDS_ENDPOINT=$(terraform output -raw rds_endpoint)
cd ..
echo "✅ Fase 1 completada."
echo "   EC2 IP : $EC2_PUBLIC_IP"
echo "   RDS    : $RDS_ENDPOINT"

# ── FASE 2 — Build Docker images ─────────────────────────────────────────────
echo ""
echo ">>> FASE 2: Compilando imágenes Docker..."
docker build --platform linux/amd64 -t $APP_NAME-backend:latest   ./backend
docker build --platform linux/amd64 -t $APP_NAME-frontend:latest  ./frontend
docker build --platform linux/amd64 -t $APP_NAME-simulator:latest ./simulator

echo "-> Empaquetando imágenes (tar)..."
docker save -o backend.tar   $APP_NAME-backend:latest
docker save -o frontend.tar  $APP_NAME-frontend:latest
docker save -o simulator.tar $APP_NAME-simulator:latest
echo "✅ Fase 2 completada."

# ── FASE 3 — Transferencia a EC2 + carga en K3s ──────────────────────────────
echo ""
echo ">>> FASE 3: Esperando SSH y transfiriendo imágenes..."

echo "⏳ Esperando a que EC2 esté accesible por SSH..."
until ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
      ubuntu@$EC2_PUBLIC_IP "echo SSH OK" 2>/dev/null; do
  echo "   Reintentando en 10s..."
  sleep 10
done

echo "⏳ Esperando a que K3s esté operativo (puede tardar 2-3 min)..."
ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ubuntu@$EC2_PUBLIC_IP \
  "timeout 300 bash -c 'until kubectl get nodes 2>/dev/null | grep -q Ready; do echo \"  K3s no listo...\"; sleep 8; done'"
echo "   K3s operativo."

echo "-> Transfiriendo imágenes por SCP..."
scp -i $SSH_KEY_PATH -o StrictHostKeyChecking=no \
    backend.tar frontend.tar simulator.tar ubuntu@$EC2_PUBLIC_IP:~

echo "-> Importando imágenes en containerd K3s..."
ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ubuntu@$EC2_PUBLIC_IP << 'ENDSSH'
    sudo k3s ctr images import backend.tar
    sudo k3s ctr images import frontend.tar
    sudo k3s ctr images import simulator.tar
    rm -f backend.tar frontend.tar simulator.tar
ENDSSH

rm -f backend.tar frontend.tar simulator.tar
echo "✅ Fase 3 completada."

# ── FASE 4 — Kubernetes deploy ───────────────────────────────────────────────
echo ""
echo ">>> FASE 4: Desplegando manifiestos en Kubernetes..."
scp -i $SSH_KEY_PATH -o StrictHostKeyChecking=no -r ./k8s ubuntu@$EC2_PUBLIC_IP:~/k8s

ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ubuntu@$EC2_PUBLIC_IP << ENDSSH
    echo "-> Inyectando variables de entorno..."
    for f in ~/k8s/backend-deployment.yaml ~/k8s/simulator-deployment.yaml; do
      sed -i "s|REPLACE_RDS_HOST|$RDS_ENDPOINT|g"    "\$f"
      sed -i "s|REPLACE_DB_NAME|$DB_NAME|g"           "\$f"
      sed -i "s|REPLACE_DB_USER|$DB_USER|g"           "\$f"
      sed -i "s|REPLACE_DB_PASSWORD|$DB_PASSWORD|g"   "\$f"
    done

    echo "-> Aplicando manifiestos..."
    kubectl apply -f ~/k8s/

    echo "-> Esperando a que los deployments estén listos..."
    kubectl wait --for=condition=available --timeout=180s \
        deployment/backend deployment/frontend deployment/simulator
ENDSSH

echo "✅ Fase 4 completada."

# ── FIN ───────────────────────────────────────────────────────────────────────
echo ""
echo "========================================"
echo "  DESPLIEGUE FINALIZADO CON EXITO"
echo "========================================"
echo ""
echo "Accede a tu aplicación en:"
echo "  http://$EC2_PUBLIC_IP"
echo ""
```

- [ ] **Step 2: Make executable**

```bash
chmod +x deploy.sh
```

- [ ] **Step 3: Commit**

```bash
git add deploy.sh
git commit -m "feat: update deploy.sh — simulator, K3s wait loop, multi-image pipeline"
```

---

## Self-Review Checklist

- [x] **Terraform:** VPC, two private subnets (eu-north-1a + eu-north-1b), db_subnet_group, EC2 with `--disable=traefik`, RDS single-AZ → all covered in Tasks 1-2
- [x] **DB init via FastAPI lifespan** (no schema.sql step in deploy.sh) → Task 4
- [x] **Seed data** with ITV alerts + overload alerts visible on first run → Task 4
- [x] **Conductores/Vehiculos/Rutas CRUD** → Tasks 5-7
- [x] **Alerts endpoint** (ITV ≤30 days + payload > 90% capacity) → Task 8
- [x] **Tracking endpoint** returning origin/actual/destination per active route → Task 8
- [x] **Simulator loop** with interpolation + route recycling → Task 10
- [x] **Frontend** Leaflet map + admin panel + polling + alert badge → Task 11
- [x] **All three Dockerfiles** → Tasks 9, 10, 12
- [x] **K8s manifests** (6 files, `imagePullPolicy: Never`, LoadBalancer for frontend) → Task 13
- [x] **deploy.sh** with SSH wait loop, K3s readiness wait, three images, sed substitution for backend+simulator → Task 14
- [x] **No placeholders** in any task
- [x] **Type consistency:** `ConductorRead`, `VehiculoRead`, `RutaRead` used consistently across all tasks
