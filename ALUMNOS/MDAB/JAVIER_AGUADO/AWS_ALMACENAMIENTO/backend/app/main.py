from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from .models import Base
from .seed import seed_database
from .routers import airplanes, flights, passengers

app = FastAPI(title="Aerodrome API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


app.include_router(airplanes.router)
app.include_router(flights.router)
app.include_router(passengers.router)


@app.get("/health")
def health():
    return {"status": "ok"}
