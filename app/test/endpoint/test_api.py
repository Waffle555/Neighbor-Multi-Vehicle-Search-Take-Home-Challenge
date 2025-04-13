from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_solve_multi_vehicle_storage():
    response = client.post("/", json=[{"length": 10, "quantity": 1}])
    assert response.status_code == 200
    assert len(response.json()) == 365

def test_empty_vehicle_list():
    response = client.post("/", json=[])
    assert response.status_code == 200
    assert len(response.json()) == 0

