from fastapi.testclient import TestClient


def _create_variant_with_stock(client: TestClient, stock: int) -> int:
    pid = client.post(
        "/products",
        json={"name": "Camiseta", "slug": f"camiseta-{stock}", "base_price": "20.00"},
    ).json()["id"]
    return client.post(
        f"/products/{pid}/variants",
        json={"size": "L", "color": "Azul", "sku": f"SKU-{stock}",
              "stock_quantity": stock},
    ).json()["id"]


def test_create_order_succeeds_and_returns_total(client: TestClient):
    variant_id = _create_variant_with_stock(client, stock=10)

    resp = client.post(
        "/orders",
        json={
            "shipping_address": "Calle Falsa 123",
            "items": [{"variant_id": variant_id, "quantity": 2}],
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["total_amount"] == "40.00"
    assert body["status"] == "pending"
    assert body["items"][0]["unit_price"] == "20.00"


def test_create_order_insufficient_stock_returns_400(client: TestClient):
    variant_id = _create_variant_with_stock(client, stock=1)

    resp = client.post(
        "/orders",
        json={"items": [{"variant_id": variant_id, "quantity": 5}]},
    )
    assert resp.status_code == 400


def test_get_order_not_found(client: TestClient):
    assert client.get("/orders/999").status_code == 404
