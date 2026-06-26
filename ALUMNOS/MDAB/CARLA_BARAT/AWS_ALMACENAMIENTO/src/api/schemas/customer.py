from pydantic import BaseModel
from typing import List
from src.api.schemas.ticket import TicketResponse


class CustomerCreate(BaseModel):
    customer_id: str
    name: str
    email: str
    phone: str
    date_of_birth: str
    membership_level: str


class CustomerResponse(CustomerCreate):
    pass


class CustomerWithHistory(CustomerResponse):
    tickets: List[TicketResponse]
    total_spent: float
