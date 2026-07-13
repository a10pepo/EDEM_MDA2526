from pydantic import BaseModel, Field
from typing import List, Optional


class TicketItemCreate(BaseModel):
    sku: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)
    discount: float = Field(ge=0, default=0.0)


class TicketItemResponse(TicketItemCreate):
    subtotal: float


class TicketCreate(BaseModel):
    cashier_id: str
    payment_method: str
    customer_id: Optional[str] = None
    items: List[TicketItemCreate] = Field(min_length=1)


class TicketStatusUpdate(BaseModel):
    status: str


class TicketResponse(BaseModel):
    ticket_id: str
    cashier_id: str
    date_time: str
    payment_method: str
    status: str
    customer_id: Optional[str]
    items: List[TicketItemResponse]
    total_amount: float
    discount_total: float
    discount_percentage: float
