def _create_airplane(client, plate="EC-F001"):
    client.post("/airplanes/", json={
        "plate_number": plate, "type": "Test",
        "last_maintenance_date": "2025-01-01",
        "next_maintenance_date": "2027-01-01",
        "capacity": 10, "owner_id": "O-1",
        "owner_name": "X", "hangar_id": "H-1",
        "fuel_capacity": 500.0,
    })


def test_create_and_list_flight(client):
    _create_airplane(client)
    payload = {
        "flight_id": "FL-TEST-001",
        "plate_number": "EC-F001",
        "arrival_time": "2026-03-01T09:00:00",
        "departure_time": "2026-03-01T14:00:00",
        "fuel_consumption": 200.0,
        "occupied_seats": 8,
        "origin": "Madrid",
        "destination": "Paris",
        "passengers": [],
    }
    response = client.post("/flights/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["flight_id"] == "FL-TEST-001"
    assert "empty_seats" in data
    assert "empty_seats_alert" in data
    assert "fuel_alert" in data

    list_response = client.get("/flights/")
    assert list_response.status_code == 200


def test_flight_not_found(client):
    response = client.get("/flights/FL-NOPE")
    assert response.status_code == 404


def test_create_flight_overbooking(client):
    _create_airplane(client, plate="EC-F003")
    payload = {
        "flight_id": "FL-TEST-003",
        "plate_number": "EC-F003",
        "arrival_time": "2026-03-01T09:00:00",
        "departure_time": "2026-03-01T14:00:00",
        "fuel_consumption": 200.0,
        "occupied_seats": 11,  # capacity is 10
        "origin": "Madrid",
        "destination": "Paris",
        "passengers": [],
    }
    response = client.post("/flights/", json=payload)
    assert response.status_code == 400


def test_create_flight_missing_airplane(client):
    payload = {
        "flight_id": "FL-TEST-002",
        "plate_number": "EC-MISSING",
        "arrival_time": "2026-03-01T09:00:00",
        "departure_time": "2026-03-01T14:00:00",
        "fuel_consumption": 200.0,
        "occupied_seats": 5,
        "origin": "Madrid",
        "destination": "Paris",
        "passengers": [],
    }
    response = client.post("/flights/", json=payload)
    assert response.status_code == 404
