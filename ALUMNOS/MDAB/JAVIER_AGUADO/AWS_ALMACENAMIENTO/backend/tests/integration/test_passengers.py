def test_create_and_list_passenger(client):
    payload = {
        "passenger_id": "P-TEST-001",
        "name": "Test User",
        "national_id": "99999999Z",
        "date_of_birth": "1990-01-01",
    }
    response = client.post("/passengers/", json=payload)
    assert response.status_code == 201
    assert response.json()["passenger_id"] == "P-TEST-001"

    list_response = client.get("/passengers/")
    assert list_response.status_code == 200
    ids = [p["passenger_id"] for p in list_response.json()]
    assert "P-TEST-001" in ids


def test_passenger_not_found(client):
    response = client.get("/passengers/P-NOPE")
    assert response.status_code == 404
