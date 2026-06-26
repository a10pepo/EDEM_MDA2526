"""
Populates the database with realistic sample data for demos.
  Local:  USE_LOCAL_DYNAMODB=true python aws/seed_data.py
  AWS:    python aws/seed_data.py
"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from src.db.dynamodb import create_tables
from src.models.product import Product
from src.models.ticket import Ticket, TicketItem
from src.models.customer import Customer
from src.services.product_service import register_product
from src.services.ticket_service import register_ticket
from src.services.customer_service import register_customer

PRODUCTS = [
    Product("ZAR-SH-001", "Slim Fit Shirt", "shirt", "M", "White", 29.95, 45, 10, "2026-05-01", "SUP-001"),
    Product("ZAR-SH-002", "Slim Fit Shirt", "shirt", "L", "Blue", 29.95, 3, 10, "2026-04-15", "SUP-001"),  # low stock
    Product("ZAR-PT-001", "Tapered Trousers", "pants", "32", "Navy", 49.95, 22, 8, "2026-05-10", "SUP-002"),
    Product("ZAR-PT-002", "Wide Leg Trousers", "pants", "34", "Beige", 55.00, 0, 5, "2026-03-20", "SUP-002"),  # OOS
    Product("ZAR-JK-001", "Structured Blazer", "jacket", "M", "Black", 89.95, 12, 5, "2026-05-20", "SUP-003"),
    Product("ZAR-SH-003", "Linen Shirt", "shirt", "S", "Green", 35.95, 30, 15, "2026-05-25", "SUP-001"),
    Product("ZAR-DR-001", "Midi Dress", "dress", "S", "Red", 59.95, 8, 10, "2026-04-30", "SUP-004"),  # low stock
    Product("ZAR-AC-001", "Canvas Belt", "accessory", "ONE", "Brown", 19.95, 60, 20, "2026-05-15", "SUP-005"),
]

CUSTOMERS = [
    Customer("DNI-001", "Laura García", "laura@email.com", "+34600111222", "1990-03-15", "gold"),
    Customer("DNI-002", "Marcos López", "marcos@email.com", "+34611222333", "1985-07-22", "silver"),
    Customer("DNI-003", "Ana Martínez", "ana@email.com", "+34622333444", "1998-11-08", "basic"),
    Customer("DNI-004", "Pedro Sánchez", "pedro@email.com", "+34633444555", "2001-01-30", "none"),
]

now = datetime.now()

TICKETS = [
    Ticket(
        "TKT-20260601-001", "CASHIER-01", (now - timedelta(days=4)).isoformat(timespec="seconds"),
        "card", "completed",
        [TicketItem("ZAR-SH-001", 2, 29.95, 0.0), TicketItem("ZAR-AC-001", 1, 19.95, 5.0)],
        "DNI-001",
    ),
    Ticket(
        "TKT-20260602-001", "CASHIER-02", (now - timedelta(days=3)).isoformat(timespec="seconds"),
        "cash", "completed",
        [TicketItem("ZAR-PT-001", 1, 49.95, 0.0)],
        "DNI-002",
    ),
    Ticket(
        "TKT-20260602-002", "CASHIER-01", (now - timedelta(days=3)).isoformat(timespec="seconds"),
        "card", "returned",
        [TicketItem("ZAR-DR-001", 1, 59.95, 0.0)],
        "DNI-003",
    ),
    Ticket(
        "TKT-20260603-001", "CASHIER-03", (now - timedelta(days=2)).isoformat(timespec="seconds"),
        "online", "completed",
        # 25% discount — will trigger HIGH_DISCOUNT alert
        [TicketItem("ZAR-JK-001", 1, 89.95, 22.50)],
        "DNI-001",
    ),
    Ticket(
        "TKT-20260604-001", "CASHIER-02", (now - timedelta(days=1)).isoformat(timespec="seconds"),
        "card", "returned",
        [TicketItem("ZAR-SH-003", 2, 35.95, 0.0)],
        None,
    ),
    Ticket(
        "TKT-20260605-001", "CASHIER-01", now.isoformat(timespec="seconds"),
        "card", "pending",
        [TicketItem("ZAR-SH-001", 1, 29.95, 0.0), TicketItem("ZAR-PT-001", 1, 49.95, 0.0)],
        "DNI-004",
    ),
]


if __name__ == "__main__":
    print("Creating tables if needed...")
    create_tables()

    print("Seeding products...")
    for p in PRODUCTS:
        register_product(p)
        print(f"  {p.sku} — {p.name}")

    print("Seeding customers...")
    for c in CUSTOMERS:
        register_customer(c)
        print(f"  {c.customer_id} — {c.name}")

    print("Seeding tickets...")
    for t in TICKETS:
        register_ticket(t)
        print(f"  {t.ticket_id} — {t.status} — €{t.total_amount():.2f}")

    print("\nSeed complete. Expected alerts:")
    print("  LOW STOCK  : ZAR-SH-002 (3 units), ZAR-PT-002 (0 units), ZAR-DR-001 (8 units)")
    print("  HIGH DISC. : TKT-20260603-001 (25% discount)")
    print("  RETURN RATE: 2/6 tickets returned = 33.3% (> 10% threshold)")
