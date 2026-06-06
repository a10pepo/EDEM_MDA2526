VEHICULO = {
    "matricula": "1234ABC", "modelo": "Mercedes Sprinter",
    "capacidad_carga_kg": 1000.0, "fecha_itv": "2026-12-31", "estado": "disponible"
}

def test_list_empty(client):
    assert client.get("/api/vehiculos").json() == []

def test_create(client):
    r = client.post("/api/vehiculos", json=VEHICULO)
    assert r.status_code == 201
    assert r.json()["matricula"] == "1234ABC"

def test_get_by_id(client):
    client.post("/api/vehiculos", json=VEHICULO)
    r = client.get("/api/vehiculos/1")
    assert r.status_code == 200
    assert r.json()["modelo"] == "Mercedes Sprinter"

def test_get_not_found(client):
    assert client.get("/api/vehiculos/999").status_code == 404

def test_update_estado(client):
    client.post("/api/vehiculos", json=VEHICULO)
    updated = {**VEHICULO, "estado": "en_ruta"}
    r = client.put("/api/vehiculos/1", json=updated)
    assert r.status_code == 200
    assert r.json()["estado"] == "en_ruta"

def test_delete(client):
    client.post("/api/vehiculos", json=VEHICULO)
    assert client.delete("/api/vehiculos/1").status_code == 204
    assert client.get("/api/vehiculos/1").status_code == 404
