from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import categories, health, orders, products
from app.core.config import get_settings
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas al arrancar (proyecto sin migraciones administradas).
    # En tests la BD la gestiona conftest, así que se omite.
    if get_settings().app_env != "test":
        init_db()
    yield


app = FastAPI(
    title="E-commerce Ropa API",
    version="0.1.0",
    description="Backend de catálogo, inventario y pedidos para una tienda de ropa.",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
