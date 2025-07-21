import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_author_success():
    payload = {"name": "テスト著者"}
    response = client.post("/authors", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "テスト著者"
    assert "id" in data

def test_create_author_missing_name():
    payload = {}
    response = client.post("/authors", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_create_author_name_too_long():
    payload = {"name": "あ" * 51}
    response = client.post("/authors", json=payload)
    assert response.status_code == 422
    assert any(
        err["loc"][-1] == "name" and "50" in err["msg"]
        for err in response.json().get("detail", [])
    )
