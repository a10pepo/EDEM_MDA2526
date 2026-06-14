import pytest
import api
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(api.app)


def test_teams_returns_200(client, monkeypatch):
    monkeypatch.setattr(api, "query", lambda sql: [{"team_id": "T-01", "name": "Red Bull Racing"}])
    assert client.get("/teams").status_code == 200


def test_teams_has_required_fields(client, monkeypatch):
    monkeypatch.setattr(api, "query", lambda sql: [{"team_id": "T-01", "name": "Red Bull Racing"}])
    data = client.get("/teams").json()
    assert "team_id" in data[0]
    assert "name" in data[0]


def test_drivers_has_required_fields(client, monkeypatch):
    monkeypatch.setattr(api, "query", lambda sql: [
        {"driver_id": "D-01", "code": "VER", "name": "Max Verstappen", "team": "Red Bull Racing"}
    ])
    data = client.get("/drivers").json()
    assert "driver_id" in data[0]
    assert "code" in data[0]
    assert "team" in data[0]


def test_races_returns_200(client, monkeypatch):
    monkeypatch.setattr(api, "query", lambda sql: [{"race_id": "R-2024-01", "name": "Bahrain GP"}])
    assert client.get("/races").status_code == 200


def test_results_has_status_field(client, monkeypatch):
    monkeypatch.setattr(api, "query", lambda sql: [
        {"race_id": "R-2024-01", "driver": "VER", "status": "Finished"}
    ])
    data = client.get("/results").json()
    assert "status" in data[0]
