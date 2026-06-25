"""Conexión a la base de datos.

La URL se lee de la variable de entorno DATABASE_URL, así el MISMO código sirve para:
  - Local con SQLite (por defecto, cero configuración):   sqlite:///./sephora_local.db
  - Local con Postgres en Docker:  postgresql+psycopg://sephora:sephora_pass@db:5432/sephora
  - AWS RDS (Postgres):            postgresql+psycopg://USER:PASS@<endpoint-rds>:5432/sephora

Para AWS solo hay que cambiar DATABASE_URL; no se toca el código.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sephora_local.db")

if DATABASE_URL.startswith("postgresql") and os.getenv("DB_SSLMODE"):
    if "sslmode=" not in DATABASE_URL:
        separator = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL = f"{DATABASE_URL}{separator}sslmode={os.getenv('DB_SSLMODE')}"

# SQLite necesita este argumento extra para usarse desde varios hilos (FastAPI).
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# pool_pre_ping evita errores por conexiones caídas (importante con RDS).
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: abre una sesión por petición y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
