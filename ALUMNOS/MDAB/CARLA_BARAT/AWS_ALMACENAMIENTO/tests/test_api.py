import os
import pytest
import boto3
from moto import mock_aws
from fastapi.testclient import TestClient

# env vars must be set before importing the app
os.environ.setdefault("USE_LOCAL_DYNAMODB", "false")
os.environ.setdefault("PRODUCTS_TABLE", "zara_products")
os.environ.setdefault("TICKETS_TABLE", "zara_tickets")
os.environ.setdefault("CUSTOMERS_TABLE", "zara_customers")

from src.api.app import app

client = TestClient(app)

PRODUCT_PAYLOAD = {
    "sku": "TST-001",
    "name": "Test Shirt",
    "category": "shirt",
    "size": "M",
    "color": "White",
    "price": 29.95,
    "stock_quantity": 20,
    "restock_threshold": 5,
    "last_restock_date": "2026-05-01",
    "supplier_id": "SUP-001",
}

TICKET_PAYLOAD = {
    "cashier_id": "C01",
    "payment_method": "card",
    "customer_id": None,
    "items": [{"sku": "TST-001", "quantity": 2, "unit_price": 29.95, "discount": 0.0}],
}

CUSTOMER_PAYLOAD = {
    "customer_id": "DNI-001",
    "name": "Test User",
    "email": "test@test.com",
    "phone": "600000000",
    "date_of_birth": "1990-01-01",
    "membership_level": "basic",
}


@pytest.fixture(autouse=True)
def mock_dynamodb(aws_env):
    with mock_aws():
        db = boto3.resource("dynamodb", region_name="us-east-1")
        for table_name, pk in [
            ("zara_products", "sku"),
            ("zara_tickets", "ticket_id"),
            ("zara_customers", "customer_id"),
        ]:
            db.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": pk, "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": pk, "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
        yield


# ── Health ────────────────────────────────────────────────────────

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── Products ──────────────────────────────────────────────────────

def test_create_product():
    r = client.post("/products/", json=PRODUCT_PAYLOAD)
    assert r.status_code == 201
    data = r.json()
    assert data["sku"] == "TST-001"
    assert data["is_below_threshold"] is False


def test_list_products_empty():
    r = client.get("/products/")
    assert r.status_code == 200
    assert r.json() == []


def test_list_products():
    client.post("/products/", json=PRODUCT_PAYLOAD)
    r = client.get("/products/")
    assert len(r.json()) == 1


def test_get_product():
    client.post("/products/", json=PRODUCT_PAYLOAD)
    r = client.get("/products/TST-001")
    assert r.status_code == 200
    assert r.json()["name"] == "Test Shirt"


def test_get_product_not_found():
    r = client.get("/products/MISSING")
    assert r.status_code == 404


def test_update_stock():
    client.post("/products/", json=PRODUCT_PAYLOAD)
    r = client.put("/products/TST-001/stock", json={"quantity": 3})
    assert r.status_code == 200
    data = r.json()
    assert data["stock_quantity"] == 3
    assert data["is_below_threshold"] is True


def test_check_stock():
    client.post("/products/", json=PRODUCT_PAYLOAD)
    r = client.get("/products/TST-001/stock")
    assert r.status_code == 200
    assert r.json()["stock_quantity"] == 20


def test_delete_product():
    client.post("/products/", json=PRODUCT_PAYLOAD)
    r = client.delete("/products/TST-001")
    assert r.status_code == 204
    assert client.get("/products/TST-001").status_code == 404


# ── Tickets ───────────────────────────────────────────────────────

def test_create_ticket():
    r = client.post("/tickets/", json=TICKET_PAYLOAD)
    assert r.status_code == 201
    data = r.json()
    assert data["total_amount"] == pytest.approx(59.90)
    assert data["status"] == "completed"
    assert len(data["items"]) == 1


def test_list_tickets_empty():
    assert client.get("/tickets/").json() == []


def test_get_ticket():
    created = client.post("/tickets/", json=TICKET_PAYLOAD).json()
    r = client.get(f"/tickets/{created['ticket_id']}")
    assert r.status_code == 200
    assert r.json()["ticket_id"] == created["ticket_id"]


def test_update_ticket_status():
    created = client.post("/tickets/", json=TICKET_PAYLOAD).json()
    r = client.put(f"/tickets/{created['ticket_id']}/status", json={"status": "returned"})
    assert r.status_code == 200
    assert r.json()["status"] == "returned"


def test_update_ticket_invalid_status():
    created = client.post("/tickets/", json=TICKET_PAYLOAD).json()
    r = client.put(f"/tickets/{created['ticket_id']}/status", json={"status": "bad"})
    assert r.status_code == 400


def test_delete_ticket():
    created = client.post("/tickets/", json=TICKET_PAYLOAD).json()
    tid = created["ticket_id"]
    assert client.delete(f"/tickets/{tid}").status_code == 204
    assert client.get(f"/tickets/{tid}").status_code == 404


# ── Customers ─────────────────────────────────────────────────────

def test_create_customer():
    r = client.post("/customers/", json=CUSTOMER_PAYLOAD)
    assert r.status_code == 201
    assert r.json()["customer_id"] == "DNI-001"


def test_get_customer_with_history():
    client.post("/customers/", json=CUSTOMER_PAYLOAD)
    ticket = {**TICKET_PAYLOAD, "customer_id": "DNI-001"}
    client.post("/tickets/", json=ticket)
    r = client.get("/customers/DNI-001")
    assert r.status_code == 200
    data = r.json()
    assert len(data["tickets"]) == 1
    assert data["total_spent"] == pytest.approx(59.90)


def test_get_customer_not_found():
    assert client.get("/customers/MISSING").status_code == 404


def test_customer_tickets_status():
    client.post("/customers/", json=CUSTOMER_PAYLOAD)
    r = client.get("/customers/DNI-001/tickets")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 0


# ── Alerts ────────────────────────────────────────────────────────

def test_alerts_empty():
    r = client.get("/alerts/")
    assert r.status_code == 200
    data = r.json()
    assert data["total_alerts"] == 0


def test_low_stock_alert_via_api():
    low_stock_product = {**PRODUCT_PAYLOAD, "stock_quantity": 2, "restock_threshold": 5}
    client.post("/products/", json=low_stock_product)
    r = client.get("/alerts/")
    data = r.json()
    assert data["total_alerts"] >= 1
    assert len(data["low_stock"]) == 1


def test_high_discount_alert_via_api():
    discounted_ticket = {
        "cashier_id": "C01",
        "payment_method": "card",
        "items": [{"sku": "TST-001", "quantity": 1, "unit_price": 100.0, "discount": 25.0}],
    }
    client.post("/tickets/", json=discounted_ticket)
    r = client.get("/alerts/")
    assert len(r.json()["high_discount"]) == 1
