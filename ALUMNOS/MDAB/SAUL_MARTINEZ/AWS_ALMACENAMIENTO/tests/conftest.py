import os

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite://")

from collections.abc import Iterator  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import app.models  # noqa: F401,E402  (registra los modelos en metadata)
from app.api.deps import get_session, get_storage  # noqa: E402
from app.main import app  # noqa: E402


class FakeStorage:
    """Sustituto de StorageService: no llama a AWS, devuelve URLs deterministas."""

    def presigned_get_url(self, key: str) -> str:
        return f"https://fake-s3.local/{key}?signature=test"

    def presigned_put_url(self, key: str, content_type: str = "image/jpeg") -> str:
        return f"https://fake-s3.local/{key}?upload=test"


@pytest.fixture(name="engine")
def engine_fixture():
    """Motor SQLite en memoria, compartido por toda la conexión del test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine) -> Iterator[Session]:
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Iterator[TestClient]:
    """Cliente HTTP con la sesión de test inyectada en lugar de la real."""

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_storage] = lambda: FakeStorage()
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
