from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import products, tickets, customers, alerts

app = FastAPI(
    title="Zara Store Management API",
    description="Sprint 3 — REST API backed by DynamoDB",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.3.0"}
