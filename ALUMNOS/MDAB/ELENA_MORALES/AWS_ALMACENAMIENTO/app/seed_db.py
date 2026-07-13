"""Crea las tablas y carga los datos de ejemplo en la base de datos.

Uso manual:
    python seed_db.py          # crea tablas y carga datos si está vacía
    python seed_db.py --reset  # borra y recrea todo desde cero

La API también llama a seed_if_empty() al arrancar, así el contenedor
queda listo para usar sin pasos manuales.
"""

import sys
from datetime import date, datetime

try:
    from .database import Base, SessionLocal, engine
    from . import models  # noqa: F401  (necesario para que se registren las tablas)
    from .seed_data import customers, orders, products
except ImportError:  # Compatibilidad si se ejecuta como script desde la carpeta app
    from database import Base, SessionLocal, engine
    import models  # noqa: F401  (necesario para que se registren las tablas)
    from seed_data import customers, orders, products


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


def seed_if_empty() -> bool:
    """Carga los datos de ejemplo solo si la tabla de productos está vacía.

    Devuelve True si insertó datos, False si ya había.
    """
    create_tables()
    db = SessionLocal()
    try:
        if db.query(models.Product).count() > 0:
            return False

        for p in products:
            db.add(models.Product(
                productCode=p["productCode"], name=p["name"], brand=p["brand"],
                category=p["category"],
                manufactureDate=date.fromisoformat(p["manufactureDate"]),
                expiryDate=date.fromisoformat(p["expiryDate"]),
                maxStock=p["maxStock"], supplierId=p["supplierId"],
                supplierName=p["supplierName"], shelfId=p["shelfId"], price=p["price"],
            ))

        for c in customers:
            db.add(models.Customer(
                customerId=c["customerId"], name=c["name"],
                nationalId=c["nationalId"],
                dateOfBirth=date.fromisoformat(c["dateOfBirth"]),
            ))

        for o in orders:
            db.add(models.Order(
                orderId=o["orderId"], productCode=o["productCode"],
                orderDate=datetime.fromisoformat(o["orderDate"]),
                shipDate=datetime.fromisoformat(o["shipDate"]),
                unitsSold=o["unitsSold"], channel=o["channel"], store=o["store"],
            ))
            for cid, status in o["customerIds"]:
                db.add(models.OrderCustomer(
                    orderId=o["orderId"], customerId=cid, status=status,
                ))

        db.commit()
        return True
    finally:
        db.close()


if __name__ == "__main__":
    if "--reset" in sys.argv:
        print("Borrando tablas...")
        drop_tables()
    inserted = seed_if_empty()
    print("Datos cargados." if inserted else "La base de datos ya tenía datos (no se tocó).")
