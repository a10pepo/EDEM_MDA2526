def test_create_and_list_airplane(client):
    payload = {
        "plate_number": "EC-TEST1",
        "type": "Cessna 172",
        "last_maintenance_date": "2025-01-01",
        "next_maintenance_date": "2027-01-01",
        "capacity": 4,
        "owner_id": "O-99999",
        "owner_name": "Test Club",
        "hangar_id": "H-99",
        "fuel_capacity": 200.0,
    }
    response = client.post("/airplanes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["plate_number"] == "EC-TEST1"
    assert "days_until_maintenance" in data
    assert "maintenance_alert" in data

    list_response = client.get("/airplanes/")
    assert list_response.status_code == 200
    plates = [a["plate_number"] for a in list_response.json()]
    assert "EC-TEST1" in plates


def test_get_airplane_not_found(client):
    response = client.get("/airplanes/EC-NOPE")
    assert response.status_code == 404


def test_create_duplicate_airplane(client):
    payload = {
        "plate_number": "EC-DUP1",
        "type": "Test",
        "last_maintenance_date": "2025-01-01",
        "next_maintenance_date": "2027-01-01",
        "capacity": 4,
        "owner_id": "O-1",
        "owner_name": "X",
        "hangar_id": "H-1",
        "fuel_capacity": 100.0,
    }
    client.post("/airplanes/", json=payload)
    response = client.post("/airplanes/", json=payload)
    assert response.status_code == 409
