import pytest

CONDUCTOR = {"dni": "12345678A", "nombre": "Juan García"}
VEHICULO  = {"matricula": "1234ABC", "modelo": "Sprinter", "capacidad_carga_kg": 1000.0, "fecha_itv": "2026-12-31"}
RUTA = {
    "vehiculo_id": 1, "conductor_id": 1,
    "origen_lat": 40.416775, "origen_lng": -3.703790,
    "destino_lat": 41.385064, "destino_lng": 2.173404,
}

@pytest.fixture
def seeded(client):
    client.post("/api/conductores", json=CONDUCTOR)
    client.post("/api/vehiculos", json=VEHICULO)
    return client

def test_list_empty(client):
    assert client.get("/api/rutas").json() == []

def test_create_sets_actual_to_origen(seeded):
    r = seeded.post("/api/rutas", json=RUTA)
    assert r.status_code == 201
    data = r.json()
    assert abs(data["actual_lat"] - 40.416775) < 1e-4
    assert abs(data["actual_lng"] - (-3.703790)) < 1e-4

def test_create_estado_default_pendiente(seeded):
    r = seeded.post("/api/rutas", json=RUTA)
    assert r.json()["estado"] == "pendiente"

def test_get_by_id(seeded):
    seeded.post("/api/rutas", json=RUTA)
    r = seeded.get("/api/rutas/1")
    assert r.status_code == 200

def test_get_not_found(client):
    assert client.get("/api/rutas/999").status_code == 404

def test_delete(seeded):
    seeded.post("/api/rutas", json=RUTA)
    assert seeded.delete("/api/rutas/1").status_code == 204
    assert seeded.get("/api/rutas/1").status_code == 404
