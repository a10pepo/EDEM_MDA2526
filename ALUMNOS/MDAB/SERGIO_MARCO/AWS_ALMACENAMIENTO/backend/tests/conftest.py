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
