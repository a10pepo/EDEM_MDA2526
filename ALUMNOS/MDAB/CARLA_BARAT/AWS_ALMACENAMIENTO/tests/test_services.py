import pytest
from src.models.product import Product
from src.models.ticket import Ticket, TicketItem
from src.models.customer import Customer
from src.services.product_service import register_product, get_product, list_products, update_stock
from src.services.ticket_service import register_ticket, get_ticket, list_tickets, update_ticket_status
from src.services.customer_service import register_customer, get_customer, list_customers
from src.services.alert_service import (
    check_low_stock_alerts,
    check_high_discount_alerts,
    check_return_rate_alert,
)


# ── Helpers ───────────────────────────────────────────────────────

def make_product(sku="SKU-001", stock=20, threshold=10) -> Product:
    return Product(
        sku=sku, name="Test Shirt", category="shirt", size="M",
        color="White", price=29.95, stock_quantity=stock,
        restock_threshold=threshold, last_restock_date="2026-05-01",
        supplier_id="SUP-001",
    )


def make_ticket(ticket_id="TKT-001", status="completed", discount=0.0) -> Ticket:
    return Ticket(
        ticket_id=ticket_id, cashier_id="C01",
        date_time="2026-06-01T10:00:00", payment_method="card",
        status=status,
        items=[TicketItem(sku="SKU-001", quantity=2, unit_price=29.95, discount=discount)],
    )


def make_customer(customer_id="DNI-001") -> Customer:
    return Customer(
        customer_id=customer_id, name="Test User",
        email="test@test.com", phone="600000000",
        date_of_birth="1990-01-01", membership_level="basic",
    )


# ── Product service ───────────────────────────────────────────────

def test_register_and_get_product(dynamodb_tables):
    product = make_product()
    assert register_product(product)
    fetched = get_product("SKU-001")
    assert fetched is not None
    assert fetched.sku == "SKU-001"
    assert fetched.stock_quantity == 20
    assert fetched.price == 29.95


def test_list_products(dynamodb_tables):
    register_product(make_product("SKU-001"))
    register_product(make_product("SKU-002"))
    products = list_products()
    assert len(products) == 2


def test_get_nonexistent_product(dynamodb_tables):
    assert get_product("MISSING") is None


def test_update_stock(dynamodb_tables):
    register_product(make_product("SKU-001", stock=20))
    assert update_stock("SKU-001", 5)
    updated = get_product("SKU-001")
    assert updated.stock_quantity == 5


def test_product_below_threshold(dynamodb_tables):
    p = make_product(stock=3, threshold=10)
    assert p.is_below_threshold()


def test_product_above_threshold(dynamodb_tables):
    p = make_product(stock=15, threshold=10)
    assert not p.is_below_threshold()


# ── Ticket service ────────────────────────────────────────────────

def test_register_and_get_ticket(dynamodb_tables):
    t = make_ticket()
    assert register_ticket(t)
    fetched = get_ticket("TKT-001")
    assert fetched is not None
    assert fetched.ticket_id == "TKT-001"
    assert fetched.status == "completed"


def test_ticket_total_amount(dynamodb_tables):
    t = make_ticket(discount=0.0)
    assert t.total_amount() == pytest.approx(59.90)


def test_ticket_discount_percentage(dynamodb_tables):
    t = make_ticket(discount=14.975)  # 25% of 59.90
    assert t.discount_percentage() == pytest.approx(25.0, abs=0.1)


def test_update_ticket_status(dynamodb_tables):
    register_ticket(make_ticket())
    assert update_ticket_status("TKT-001", "returned")
    updated = get_ticket("TKT-001")
    assert updated.status == "returned"


def test_update_ticket_invalid_status(dynamodb_tables):
    register_ticket(make_ticket())
    assert not update_ticket_status("TKT-001", "invalid_status")


def test_list_tickets(dynamodb_tables):
    register_ticket(make_ticket("TKT-001"))
    register_ticket(make_ticket("TKT-002"))
    assert len(list_tickets()) == 2


# ── Customer service ──────────────────────────────────────────────

def test_register_and_get_customer(dynamodb_tables):
    c = make_customer()
    assert register_customer(c)
    fetched = get_customer("DNI-001")
    assert fetched is not None
    assert fetched.name == "Test User"
    assert fetched.membership_level == "basic"


def test_list_customers(dynamodb_tables):
    register_customer(make_customer("DNI-001"))
    register_customer(make_customer("DNI-002"))
    assert len(list_customers()) == 2


# ── Alert service ─────────────────────────────────────────────────

def test_low_stock_alert_triggers(dynamodb_tables):
    register_product(make_product("SKU-001", stock=3, threshold=10))
    alerts = check_low_stock_alerts()
    assert len(alerts) == 1
    assert alerts[0]["type"] == "LOW_STOCK"
    assert alerts[0]["sku"] == "SKU-001"


def test_low_stock_alert_no_trigger(dynamodb_tables):
    register_product(make_product("SKU-001", stock=20, threshold=10))
    assert check_low_stock_alerts() == []


def test_high_discount_alert_triggers(dynamodb_tables):
    t = make_ticket(discount=15.0)  # 15/59.90 ≈ 25%
    register_ticket(t)
    alerts = check_high_discount_alerts()
    assert len(alerts) == 1
    assert alerts[0]["type"] == "HIGH_DISCOUNT"


def test_high_discount_alert_no_trigger(dynamodb_tables):
    t = make_ticket(discount=0.0)
    register_ticket(t)
    assert check_high_discount_alerts() == []


def test_return_rate_alert_triggers(dynamodb_tables):
    register_ticket(make_ticket("TKT-001", status="returned"))
    register_ticket(make_ticket("TKT-002", status="returned"))
    register_ticket(make_ticket("TKT-003", status="completed"))
    alerts = check_return_rate_alert()
    assert len(alerts) == 1
    assert alerts[0]["type"] == "HIGH_RETURN_RATE"
    assert alerts[0]["rate_pct"] == pytest.approx(66.7, abs=0.1)


def test_return_rate_alert_no_trigger(dynamodb_tables):
    register_ticket(make_ticket("TKT-001", status="completed"))
    register_ticket(make_ticket("TKT-002", status="completed"))
    assert check_return_rate_alert() == []


def test_no_alerts_on_empty_db(dynamodb_tables):
    assert check_low_stock_alerts() == []
    assert check_high_discount_alerts() == []
    assert check_return_rate_alert() == []
