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

def create_test_author():
    payload = {"name": "ユニットテスト著者"}
    response = client.post("/authors", json=payload)
    assert response.status_code == 200
    return response.json()["id"]

def test_create_book_success():
    author_id = create_test_author()
    payload = {"title": "テスト本", "author_id": author_id}
    response = client.post("/books", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "テスト本"
    assert data["author_id"] == author_id
    assert data["author_name"] == "ユニットテスト著者"
    assert "id" in data

def test_create_book_missing_title():
    author_id = create_test_author()
    payload = {"author_id": author_id}
    response = client.post("/books", json=payload)
    assert response.status_code == 422

def test_create_book_title_too_long():
    author_id = create_test_author()
    payload = {"title": "あ" * 101, "author_id": author_id}
    response = client.post("/books", json=payload)
    assert response.status_code == 422
    assert any(
        err["loc"][-1] == "title" and "100" in err["msg"]
        for err in response.json().get("detail", [])
    )

def test_get_books():
    author_id = create_test_author()
    payload = {"title": "取得テスト本", "author_id": author_id}
    client.post("/books", json=payload)
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(book["title"] == "取得テスト本" for book in data)
    assert any(book["title"] == "取得テスト本" and book["author_name"] == "ユニットテスト著者" for book in data)

def test_get_book_by_id():
    author_id = create_test_author()
    payload = {"title": "ID取得テスト本", "author_id": author_id}
    response = client.post("/books", json=payload)
    book_id = response.json()["id"]
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == "ID取得テスト本"

def test_get_book_not_found():
    response = client.get("/books/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

def test_delete_book_success():
    author_id = create_test_author()
    payload = {"title": "削除テスト本", "author_id": author_id}
    response = client.post("/books", json=payload)
    book_id = response.json()["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404

def test_delete_book_not_found():
    response = client.delete("/books/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
