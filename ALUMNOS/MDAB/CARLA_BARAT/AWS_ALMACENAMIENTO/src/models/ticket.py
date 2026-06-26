from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TicketItem:
    sku: str
    quantity: int
    unit_price: float
    discount: float

    def subtotal(self) -> float:
        return round((self.unit_price * self.quantity) - self.discount, 2)


@dataclass
class Ticket:
    ticket_id: str
    cashier_id: str
    date_time: str  # ISO datetime string
    payment_method: str  # cash, card, online
    status: str  # pending, completed, returned
    items: List[TicketItem] = field(default_factory=list)
    customer_id: Optional[str] = None

    def total_amount(self) -> float:
        return round(sum(i.subtotal() for i in self.items), 2)

    def discount_total(self) -> float:
        return round(sum(i.discount for i in self.items), 2)

    def discount_percentage(self) -> float:
        gross = sum(i.unit_price * i.quantity for i in self.items)
        if gross == 0:
            return 0.0
        return round((self.discount_total() / gross) * 100, 2)

    def to_dynamodb_item(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "cashier_id": self.cashier_id,
            "date_time": self.date_time,
            "payment_method": self.payment_method,
            "status": self.status,
            "customer_id": self.customer_id or "",
            "items": [
                {
                    "sku": i.sku,
                    "quantity": i.quantity,
                    "unit_price": str(i.unit_price),
                    "discount": str(i.discount),
                }
                for i in self.items
            ],
        }

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> "Ticket":
        items = [
            TicketItem(
                sku=i["sku"],
                quantity=int(i["quantity"]),
                unit_price=float(i["unit_price"]),
                discount=float(i["discount"]),
            )
            for i in item.get("items", [])
        ]
        return cls(
            ticket_id=item["ticket_id"],
            cashier_id=item["cashier_id"],
            date_time=item["date_time"],
            payment_method=item["payment_method"],
            status=item["status"],
            customer_id=item.get("customer_id") or None,
            items=items,
        )
