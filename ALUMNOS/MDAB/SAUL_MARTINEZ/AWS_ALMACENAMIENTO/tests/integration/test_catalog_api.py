from fastapi.testclient import TestClient


def test_health(client: TestClient):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_get_category(client: TestClient):
    resp = client.post("/categories", json={"name": "Hombre", "slug": "hombre"})
    assert resp.status_code == 201
    cat_id = resp.json()["id"]

    assert client.get(f"/categories/{cat_id}").json()["name"] == "Hombre"
    assert len(client.get("/categories").json()) == 1


def test_duplicate_category_slug_conflicts(client: TestClient):
    client.post("/categories", json={"name": "Hombre", "slug": "hombre"})
    resp = client.post("/categories", json={"name": "Otro", "slug": "hombre"})
    assert resp.status_code == 409


def test_product_lifecycle_with_variant_and_image(client: TestClient):
    # Crear producto
    resp = client.post(
        "/products",
        json={"name": "Camiseta", "slug": "camiseta", "base_price": "19.99"},
    )
    assert resp.status_code == 201
    pid = resp.json()["id"]

    # Añadir variante
    resp = client.post(
        f"/products/{pid}/variants",
        json={"size": "M", "color": "Negro", "sku": "CAM-M-NEG", "stock_quantity": 5},
    )
    assert resp.status_code == 201
    assert resp.json()["effective_price"] == "19.99"

    # Registrar imagen (devuelve URL prefirmada del FakeStorage)
    resp = client.post(
        f"/products/{pid}/images",
        json={"s3_key": "productos/1/foto.jpg", "is_primary": True},
    )
    assert resp.status_code == 201
    assert resp.json()["url"].startswith("https://fake-s3.local/")

    # Detalle del producto
    detail = client.get(f"/products/{pid}").json()
    assert len(detail["variants"]) == 1
    assert len(detail["images"]) == 1


def test_presign_upload_url(client: TestClient):
    pid = client.post(
        "/products",
        json={"name": "Pantalón", "slug": "pantalon", "base_price": "39.90"},
    ).json()["id"]

    resp = client.post(
        f"/products/{pid}/images/presign",
        json={"s3_key": "productos/2/foto.jpg", "content_type": "image/png"},
    )
    assert resp.status_code == 200
    assert resp.json()["upload_url"].startswith("https://fake-s3.local/")


def test_list_products_filters_by_category(client: TestClient):
    cat = client.post("/categories", json={"name": "Mujer", "slug": "mujer"}).json()
    client.post(
        "/products",
        json={"name": "Falda", "slug": "falda", "base_price": "25.00",
              "category_id": cat["id"]},
    )
    client.post(
        "/products", json={"name": "Gorra", "slug": "gorra", "base_price": "10.00"}
    )

    filtered = client.get(f"/products?category_id={cat['id']}").json()
    assert len(filtered) == 1
    assert filtered[0]["name"] == "Falda"
