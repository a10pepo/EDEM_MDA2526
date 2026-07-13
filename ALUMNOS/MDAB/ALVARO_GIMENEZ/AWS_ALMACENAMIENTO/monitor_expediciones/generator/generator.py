import os
import random
import time
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "almacen_db")
DB_USER = os.getenv("DB_USER", "almacen_user")
DB_PASS = os.getenv("DB_PASS", "almacen_pass")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"


class Base(DeclarativeBase):
    pass


class MaestroProducto(Base):
    __tablename__ = "maestro_productos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    categoria = Column(String(50))
    precio_unitario = Column(Numeric(10, 2))


class MaestroCliente(Base):
    __tablename__ = "maestro_clientes"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    empresa = Column(String(100))
    ciudad = Column(String(50))


class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("maestro_productos.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("maestro_clientes.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_expedicion = Column(DateTime, default=datetime.utcnow)


def wait_for_db(engine, retries=15, delay=5):
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Conexión a la base de datos establecida.")
            return
        except Exception as e:
            print(f"Intento {attempt}/{retries}: BD no disponible ({e}). Reintentando en {delay}s...")
            time.sleep(delay)
    raise RuntimeError("No se pudo conectar a la base de datos tras varios intentos.")


def main():
    engine = create_engine(DATABASE_URL)
    wait_for_db(engine)

    with Session(engine) as session:
        producto_ids = [row.id for row in session.query(MaestroProducto.id).all()]
        cliente_ids = [row.id for row in session.query(MaestroCliente.id).all()]

    print("Generador iniciado. Insertando transacciones cada 10 segundos...")

    while True:
        with Session(engine) as session:
            tx = Transaccion(
                producto_id=random.choice(producto_ids),
                cliente_id=random.choice(cliente_ids),
                cantidad=random.randint(1, 50),
            )
            session.add(tx)
            session.commit()
            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] Transacción insertada — "
                f"producto_id={tx.producto_id}, cliente_id={tx.cliente_id}, cantidad={tx.cantidad}"
            )

        time.sleep(10)


if __name__ == "__main__":
    main()
