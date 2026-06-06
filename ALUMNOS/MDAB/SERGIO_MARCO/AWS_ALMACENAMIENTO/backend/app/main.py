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
