from fastapi import APIRouter, HTTPException
from typing import List

from src.api.schemas.customer import CustomerCreate, CustomerResponse, CustomerWithHistory
from src.api.routers.tickets import _to_response as ticket_to_response
from src.models.customer import Customer
from src.services.customer_service import (
    delete_customer,
    get_customer,
    list_customers,
    register_customer,
)
from src.services.ticket_service import list_tickets

router = APIRouter()


@router.get("/", response_model=List[CustomerResponse])
def list_all():
    return [c.__dict__ for c in list_customers()]


@router.post("/", response_model=CustomerResponse, status_code=201)
def create(data: CustomerCreate):
    customer = Customer(**data.model_dump())
    if not register_customer(customer):
        raise HTTPException(500, "Failed to register customer")
    return customer.__dict__


@router.get("/{customer_id}", response_model=CustomerWithHistory)
def get_one(customer_id: str):
    c = get_customer(customer_id)
    if not c:
        raise HTTPException(404, f"Customer '{customer_id}' not found")
    tickets = [t for t in list_tickets() if t.customer_id == customer_id]
    total_spent = sum(t.total_amount() for t in tickets if t.status != "returned")
    return {
        **c.__dict__,
        "tickets": [ticket_to_response(t) for t in tickets],
        "total_spent": round(total_spent, 2),
    }


@router.get("/{customer_id}/tickets")
def get_tickets(customer_id: str):
    if not get_customer(customer_id):
        raise HTTPException(404, f"Customer '{customer_id}' not found")
    tickets = [t for t in list_tickets() if t.customer_id == customer_id]
    returned = sum(1 for t in tickets if t.status == "returned")
    completed = sum(1 for t in tickets if t.status == "completed")
    pending = sum(1 for t in tickets if t.status == "pending")
    return {
        "customer_id": customer_id,
        "total": len(tickets),
        "completed": completed,
        "pending": pending,
        "returned": returned,
        "tickets": [ticket_to_response(t) for t in tickets],
    }


@router.delete("/{customer_id}", status_code=204)
def remove(customer_id: str):
    if not get_customer(customer_id):
        raise HTTPException(404, f"Customer '{customer_id}' not found")
    delete_customer(customer_id)
