from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings

settings = get_settings()

# pool_pre_ping evita conexiones muertas tras inactividad (típico en contenedores).
engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)


def init_db() -> None:
    """Crea las tablas a partir de los modelos SQLModel.

    Para este proyecto (coste 0, sin RDS administrado) usamos create_all en el
    arranque en lugar de migraciones Alembic. Si el esquema crece, se puede
    introducir Alembic sin cambiar los modelos.
    """
    # Importa los modelos para que queden registrados en SQLModel.metadata.
    import app.models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Dependencia de FastAPI: una sesión por request."""
    with Session(engine) as session:
        yield session
