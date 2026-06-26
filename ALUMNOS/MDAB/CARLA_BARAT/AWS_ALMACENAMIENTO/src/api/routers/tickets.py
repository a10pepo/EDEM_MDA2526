from datetime import datetime

from fastapi import APIRouter, HTTPException
from typing import List

from src.api.schemas.ticket import TicketCreate, TicketResponse, TicketStatusUpdate
from src.models.ticket import Ticket, TicketItem
from src.services.ticket_service import (
    _generate_ticket_id,
    delete_ticket,
    get_ticket,
    list_tickets,
    register_ticket,
    update_ticket_status,
)

router = APIRouter()


def _to_response(t: Ticket) -> dict:
    return {
        "ticket_id": t.ticket_id,
        "cashier_id": t.cashier_id,
        "date_time": t.date_time,
        "payment_method": t.payment_method,
        "status": t.status,
        "customer_id": t.customer_id,
        "items": [
            {
                "sku": i.sku,
                "quantity": i.quantity,
                "unit_price": i.unit_price,
                "discount": i.discount,
                "subtotal": i.subtotal(),
            }
            for i in t.items
        ],
        "total_amount": t.total_amount(),
        "discount_total": t.discount_total(),
        "discount_percentage": t.discount_percentage(),
    }


@router.get("/", response_model=List[TicketResponse])
def list_all():
    return [_to_response(t) for t in list_tickets()]


@router.post("/", response_model=TicketResponse, status_code=201)
def create(data: TicketCreate):
    ticket = Ticket(
        ticket_id=_generate_ticket_id(),
        cashier_id=data.cashier_id,
        date_time=datetime.now().isoformat(timespec="seconds"),
        payment_method=data.payment_method,
        status="completed",
        customer_id=data.customer_id,
        items=[
            TicketItem(
                sku=i.sku,
                quantity=i.quantity,
                unit_price=i.unit_price,
                discount=i.discount,
            )
            for i in data.items
        ],
    )
    if not register_ticket(ticket):
        raise HTTPException(500, "Failed to register ticket")
    return _to_response(ticket)


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_one(ticket_id: str):
    t = get_ticket(ticket_id)
    if not t:
        raise HTTPException(404, f"Ticket '{ticket_id}' not found")
    return _to_response(t)


@router.put("/{ticket_id}/status", response_model=TicketResponse)
def update_status(ticket_id: str, body: TicketStatusUpdate):
    t = get_ticket(ticket_id)
    if not t:
        raise HTTPException(404, f"Ticket '{ticket_id}' not found")
    if not update_ticket_status(ticket_id, body.status):
        raise HTTPException(400, f"Invalid status '{body.status}'. Use: pending / completed / returned")
    t.status = body.status
    return _to_response(t)


@router.delete("/{ticket_id}", status_code=204)
def remove(ticket_id: str):
    if not get_ticket(ticket_id):
        raise HTTPException(404, f"Ticket '{ticket_id}' not found")
    delete_ticket(ticket_id)
