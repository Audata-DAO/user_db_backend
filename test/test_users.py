from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
