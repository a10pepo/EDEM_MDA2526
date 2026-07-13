"""API REST de la tienda Sephora (FastAPI + base de datos).

Expone las 12 funcionalidades del MVP como endpoints HTTP, ahora con
PERSISTENCIA en una base de datos relacional (SQLite en local, RDS/Postgres en AWS).
Los datos ya NO se pierden al reiniciar.

Documentación interactiva automática en /docs (Swagger UI).
"""

from contextlib import asynccontextmanager
from datetime import date, datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

try:
    from . import models
    from .database import engine, get_db
    from .schemas import CustomerIn, OrderIn, ProductIn
    from .seed_db import seed_if_empty
except ImportError:  # Compatibilidad si se ejecuta como script desde la carpeta app
    import importlib
    import pathlib
    import sys

    package_root = pathlib.Path(__file__).resolve().parent
    if str(package_root) not in sys.path:
        sys.path.insert(0, str(package_root))

    import models
    from database import engine, get_db
    from schemas import CustomerIn, OrderIn, ProductIn
    from seed_db import seed_if_empty

DIAS_ALERTA_CADUCIDAD = 100
UMBRAL_ALERTA = 0.10


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al arrancar: crear tablas y cargar datos de ejemplo si la BD está vacía.
    models.Base.metadata.create_all(engine)
    seed_if_empty()
    yield


app = FastAPI(
    title="Sephora Store API",
    description="Gestión de productos, pedidos y clientes de la tienda Sephora (con base de datos).",
    version="2.0.0",
    lifespan=lifespan,
)


# --------------------------------------------------------------------------
# Serializadores (ORM -> dict)
# --------------------------------------------------------------------------
def product_to_dict(p: models.Product) -> dict:
    return {
        "productCode": p.productCode, "name": p.name, "brand": p.brand,
        "category": p.category, "manufactureDate": p.manufactureDate,
        "expiryDate": p.expiryDate, "maxStock": p.maxStock,
        "supplierId": p.supplierId, "supplierName": p.supplierName,
        "shelfId": p.shelfId, "price": p.price,
    }


def order_to_dict(o: models.Order) -> dict:
    return {
        "orderId": o.orderId, "productCode": o.productCode,
        "orderDate": o.orderDate, "shipDate": o.shipDate,
        "unitsSold": o.unitsSold, "channel": o.channel, "store": o.store,
        "customerIds": [[oc.customerId, oc.status] for oc in o.order_customers],
    }


def customer_to_dict(c: models.Customer) -> dict:
    return {
        "customerId": c.customerId, "name": c.name,
        "nationalId": c.nationalId, "dateOfBirth": c.dateOfBirth,
    }


def units_sold_by_product(db: Session) -> dict:
    """Devuelve {productCode: unidades vendidas} agregando todos los pedidos."""
    rows = db.query(models.Order.productCode, func.coalesce(func.sum(models.Order.unitsSold), 0)) \
             .group_by(models.Order.productCode).all()
    return {code: total for code, total in rows}


# --------------------------------------------------------------------------
# Raíz / salud
# --------------------------------------------------------------------------
@app.get("/", tags=["info"])
def root(db: Session = Depends(get_db)):
    return {
        "app": "Sephora Store API",
        "docs": "/docs",
        "productos": db.query(models.Product).count(),
        "pedidos": db.query(models.Order).count(),
        "clientes": db.query(models.Customer).count(),
    }


@app.get("/health", tags=["info"])
def health():
    return {"status": "ok"}


# --------------------------------------------------------------------------
# 1-3  LISTAR
# --------------------------------------------------------------------------
@app.get("/products", tags=["listar"])
def list_products(db: Session = Depends(get_db)):
    return [product_to_dict(p) for p in db.query(models.Product).all()]


@app.get("/orders", tags=["listar"])
def list_orders(db: Session = Depends(get_db)):
    return [order_to_dict(o) for o in db.query(models.Order).all()]


@app.get("/customers", tags=["listar"])
def list_customers(db: Session = Depends(get_db)):
    return [customer_to_dict(c) for c in db.query(models.Customer).all()]


# --------------------------------------------------------------------------
# 4-6  REGISTRAR
# --------------------------------------------------------------------------
@app.post("/products", status_code=201, tags=["registrar"])
def register_product(product: ProductIn, db: Session = Depends(get_db)):
    if db.get(models.Product, product.productCode):
        raise HTTPException(409, f"El producto {product.productCode} ya existe.")
    p = models.Product(
        productCode=product.productCode, name=product.name, brand=product.brand,
        category=product.category,
        manufactureDate=date.fromisoformat(product.manufactureDate),
        expiryDate=date.fromisoformat(product.expiryDate),
        maxStock=product.maxStock, supplierId=product.supplierId,
        supplierName=product.supplierName, shelfId=product.shelfId, price=product.price,
    )
    db.add(p)
    db.commit()
    return {"message": f"Producto {product.productCode} registrado.", "product": product_to_dict(p)}


@app.post("/orders", status_code=201, tags=["registrar"])
def register_order(order: OrderIn, db: Session = Depends(get_db)):
    if db.get(models.Order, order.orderId):
        raise HTTPException(409, f"El pedido {order.orderId} ya existe.")
    if not db.get(models.Product, order.productCode):
        raise HTTPException(404, f"El producto {order.productCode} no existe.")
    o = models.Order(
        orderId=order.orderId, productCode=order.productCode,
        orderDate=datetime.fromisoformat(order.orderDate),
        shipDate=datetime.fromisoformat(order.shipDate),
        unitsSold=order.unitsSold, channel=order.channel, store=order.store,
    )
    db.add(o)
    for c in order.customers:
        db.add(models.OrderCustomer(orderId=order.orderId, customerId=c.customerId, status=c.status))
    db.commit()
    db.refresh(o)
    return {"message": f"Pedido {order.orderId} registrado.", "order": order_to_dict(o)}


@app.post("/customers", status_code=201, tags=["registrar"])
def register_customer(customer: CustomerIn, db: Session = Depends(get_db)):
    if db.get(models.Customer, customer.customerId):
        raise HTTPException(409, f"El cliente {customer.customerId} ya existe.")
    c = models.Customer(
        customerId=customer.customerId, name=customer.name,
        nationalId=customer.nationalId,
        dateOfBirth=date.fromisoformat(customer.dateOfBirth),
    )
    db.add(c)
    db.commit()
    return {"message": f"Cliente {customer.customerId} registrado.", "customer": customer_to_dict(c)}


# --------------------------------------------------------------------------
# 7-9  CÁLCULOS
# --------------------------------------------------------------------------
@app.get("/products/availability", tags=["calcular"])
def availability(db: Session = Depends(get_db)):
    sold = units_sold_by_product(db)
    result = []
    for p in db.query(models.Product).all():
        s = sold.get(p.productCode, 0)
        result.append({
            "productCode": p.productCode, "name": p.name,
            "maxStock": p.maxStock, "unitsSold": s, "available": p.maxStock - s,
        })
    return result


@app.get("/products/{product_code}/days-until-expiry", tags=["calcular"])
def days_until_expiry(product_code: str, db: Session = Depends(get_db)):
    p = db.get(models.Product, product_code)
    if not p:
        raise HTTPException(404, "Producto no encontrado.")
    d = (p.expiryDate - date.today()).days
    return {
        "productCode": product_code, "name": p.name, "expiryDate": p.expiryDate,
        "daysUntilExpiry": d, "expired": d < 0,
    }


@app.get("/orders/{order_id}/status", tags=["calcular"])
def order_status(order_id: str, db: Session = Depends(get_db)):
    o = db.get(models.Order, order_id)
    if not o:
        raise HTTPException(404, "Pedido no encontrado.")
    return {
        "orderId": order_id,
        "customers": [{"customerId": oc.customerId, "status": oc.status} for oc in o.order_customers],
        "summary": {
            "confirmed": sum(1 for oc in o.order_customers if oc.status == "Confirmed"),
            "cancelled": sum(1 for oc in o.order_customers if oc.status == "Cancelled"),
            "returned": sum(1 for oc in o.order_customers if oc.status == "Returned"),
        },
    }


# --------------------------------------------------------------------------
# 10-12  ALERTAS
# --------------------------------------------------------------------------
@app.get("/alerts/low-stock", tags=["alertas"])
def alert_low_stock(db: Session = Depends(get_db)):
    sold = units_sold_by_product(db)
    alerts = []
    for p in db.query(models.Product).all():
        available = p.maxStock - sold.get(p.productCode, 0)
        if available < p.maxStock * UMBRAL_ALERTA:
            alerts.append({
                "productCode": p.productCode, "name": p.name,
                "available": available, "maxStock": p.maxStock,
            })
    return {"threshold": "10% del stock máximo", "alerts": alerts}


@app.get("/alerts/expiry-soon", tags=["alertas"])
def alert_expiry_soon(db: Session = Depends(get_db)):
    alerts = []
    for p in db.query(models.Product).all():
        d = (p.expiryDate - date.today()).days
        if d < DIAS_ALERTA_CADUCIDAD:
            alerts.append({
                "productCode": p.productCode, "name": p.name,
                "expiryDate": p.expiryDate, "daysUntilExpiry": d, "expired": d < 0,
            })
    return {"thresholdDays": DIAS_ALERTA_CADUCIDAD, "alerts": alerts}


@app.get("/alerts/big-orders", tags=["alertas"])
def alert_big_orders(db: Session = Depends(get_db)):
    alerts = []
    for o in db.query(models.Order).all():
        p = o.product
        if p and o.unitsSold > p.maxStock * UMBRAL_ALERTA:
            alerts.append({
                "orderId": o.orderId, "productCode": o.productCode, "name": p.name,
                "unitsSold": o.unitsSold, "maxStock": p.maxStock,
            })
    return {"threshold": "10% del stock máximo", "alerts": alerts}
