from datetime import date, timedelta

def _seed(client):
    client.post("/api/conductores", json={"dni": "12345678A", "nombre": "Juan"})
    client.post("/api/vehiculos", json={
        "matricula": "ITV001", "modelo": "Sprinter",
        "capacidad_carga_kg": 1000.0,
        "fecha_itv": str(date.today() + timedelta(days=15)),
        "estado": "disponible"
    })
    client.post("/api/vehiculos", json={
        "matricula": "OK001", "modelo": "Transit",
        "capacidad_carga_kg": 1000.0,
        "fecha_itv": str(date.today() + timedelta(days=90)),
        "estado": "en_ruta"
    })

def test_itv_alert_triggered(client):
    _seed(client)
    r = client.get("/api/alerts")
    assert r.status_code == 200
    assert any(a["matricula"] == "ITV001" for a in r.json()["itv"])

def test_no_alert_for_distant_itv(client):
    _seed(client)
    r = client.get("/api/alerts")
    assert not any(a["matricula"] == "OK001" for a in r.json()["itv"])

def test_alerts_structure(client):
    r = client.get("/api/alerts")
    assert "itv" in r.json()
    assert "sobrecarga" in r.json()
