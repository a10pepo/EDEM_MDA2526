def test_list_empty(client):
    r = client.get("/api/conductores")
    assert r.status_code == 200
    assert r.json() == []

def test_create(client):
    r = client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan García", "telefono": "600111222"})
    assert r.status_code == 201
    data = r.json()
    assert data["dni"] == "12345678A"
    assert data["id"] is not None

def test_get_by_id(client):
    client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan García"})
    r = client.get("/api/conductores/1")
    assert r.status_code == 200
    assert r.json()["nombre"] == "Juan García"

def test_get_not_found(client):
    assert client.get("/api/conductores/999").status_code == 404

def test_update(client):
    client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan García"})
    r = client.put("/api/conductores/1", json={"dni": "12345678A", "nombre": "Juan Modificado"})
    assert r.status_code == 200
    assert r.json()["nombre"] == "Juan Modificado"

def test_delete(client):
    client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan García"})
    assert client.delete("/api/conductores/1").status_code == 204
    assert client.get("/api/conductores/1").status_code == 404
