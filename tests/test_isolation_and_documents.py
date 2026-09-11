import io

from tests.conftest import register_and_login


def test_user_cannot_list_other_users_documents(client):
    headers_a = register_and_login(client, "alice@isolation.com", "StrongPass123")
    headers_b = register_and_login(client, "bob@isolation.com", "StrongPass123")

    client.post(
        "/api/v1/documents",
        headers=headers_a,
        files={"file": ("alice.txt", io.BytesIO(b"Alice's private content"), "text/plain")},
    )

    resp_b = client.get("/api/v1/documents", headers=headers_b)
    assert resp_b.status_code == 200
    assert resp_b.json()["items"] == []


def test_user_cannot_fetch_other_users_document_by_id(client):
    headers_a = register_and_login(client, "carol@isolation.com", "StrongPass123")
    headers_b = register_and_login(client, "dave@isolation.com", "StrongPass123")

    upload = client.post(
        "/api/v1/documents",
        headers=headers_a,
        files={"file": ("carol.txt", io.BytesIO(b"Carol's private content"), "text/plain")},
    )
    doc_id = upload.json()["id"]

    resp = client.get(f"/api/v1/documents/{doc_id}", headers=headers_b)
    assert resp.status_code == 404


def test_user_cannot_delete_other_users_document(client):
    headers_a = register_and_login(client, "erin@isolation.com", "StrongPass123")
    headers_b = register_and_login(client, "frank@isolation.com", "StrongPass123")

    upload = client.post(
        "/api/v1/documents",
        headers=headers_a,
        files={"file": ("erin.txt", io.BytesIO(b"Erin's private content"), "text/plain")},
    )
    doc_id = upload.json()["id"]

    resp = client.delete(f"/api/v1/documents/{doc_id}", headers=headers_b)
    assert resp.status_code == 404

    still_there = client.get(f"/api/v1/documents/{doc_id}", headers=headers_a)
    assert still_there.status_code == 200


def test_user_cannot_access_other_users_conversation(client):
    headers_a = register_and_login(client, "gina@isolation.com", "StrongPass123")
    headers_b = register_and_login(client, "hank@isolation.com", "StrongPass123")

    chat_resp = client.post(
        "/api/v1/chat", headers=headers_a, json={"question": "What is in my document?"}
    )
    conv_id = chat_resp.json()["conversation_id"]

    resp = client.get(f"/api/v1/conversations/{conv_id}", headers=headers_b)
    assert resp.status_code == 404


def test_duplicate_upload_rejected(client):
    headers = register_and_login(client, "ivan@isolation.com", "StrongPass123")
    content = io.BytesIO(b"same content twice")
    client.post(
        "/api/v1/documents", headers=headers, files={"file": ("f1.txt", content, "text/plain")}
    )
    content.seek(0)
    resp = client.post(
        "/api/v1/documents", headers=headers, files={"file": ("f2.txt", content, "text/plain")}
    )
    assert resp.status_code == 409


def test_unsupported_file_type_rejected(client):
    headers = register_and_login(client, "judy@isolation.com", "StrongPass123")
    resp = client.post(
        "/api/v1/documents",
        headers=headers,
        files={"file": ("virus.exe", io.BytesIO(b"binary"), "application/octet-stream")},
    )
    assert resp.status_code == 415


def test_empty_file_rejected(client):
    headers = register_and_login(client, "kyle@isolation.com", "StrongPass123")
    resp = client.post(
        "/api/v1/documents",
        headers=headers,
        files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")},
    )
    assert resp.status_code == 400
