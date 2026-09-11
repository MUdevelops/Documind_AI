from tests.conftest import register_and_login


def test_register_creates_user(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "StrongPass123", "full_name": "Alice"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "alice@example.com"
    assert "hashed_password" not in body


def test_register_duplicate_email_rejected(client):
    payload = {"email": "bob@example.com", "password": "StrongPass123"}
    client.post("/api/v1/auth/register", json=payload)
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_success_returns_tokens(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "carol@example.com", "password": "StrongPass123"},
    )
    resp = client.post(
        "/api/v1/auth/login", json={"email": "carol@example.com", "password": "StrongPass123"}
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password_rejected(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "dave@example.com", "password": "StrongPass123"},
    )
    resp = client.post(
        "/api/v1/auth/login", json={"email": "dave@example.com", "password": "WrongPass"}
    )
    assert resp.status_code == 401


def test_protected_endpoint_requires_token(client):
    resp = client.get("/api/v1/documents")
    assert resp.status_code == 401


def test_protected_endpoint_with_token_succeeds(client):
    headers = register_and_login(client)
    resp = client.get("/api/v1/documents", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["items"] == []
