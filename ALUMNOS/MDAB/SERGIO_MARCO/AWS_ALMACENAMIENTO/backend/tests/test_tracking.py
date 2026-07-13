def _seed_active_route(client):
    client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan"})
    client.post("/api/vehiculos", json={
        "matricula": "1234ABC", "modelo": "Sprinter",
        "capacidad_carga_kg": 1000.0, "fecha_itv": "2027-12-31"
    })
    client.post("/api/rutas", json={
        "vehiculo_id": 1, "conductor_id": 1,
        "origen_lat": 40.416775, "origen_lng": -3.703790,
        "destino_lat": 41.385064, "destino_lng": 2.173404,
        "estado": "en_ruta"
    })

def test_active_routes_empty(client):
    r = client.get("/api/routes/active")
    assert r.status_code == 200
    assert r.json() == []

def test_active_routes_returns_en_ruta_only(client):
    _seed_active_route(client)
    r = client.get("/api/routes/active")
    assert len(r.json()) == 1

def test_active_route_shape(client):
    _seed_active_route(client)
    route = client.get("/api/routes/active").json()[0]
    assert "lat" in route["origen"]
    assert "lng" in route["origen"]
    assert "lat" in route["actual"]
    assert "lng" in route["destino"]
