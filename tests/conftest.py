import os
import shutil
import tempfile

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci-only-not-for-prod-use")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture()
def tmp_data_dirs(monkeypatch):
    tmp_dir = tempfile.mkdtemp()
    monkeypatch.setenv("VECTOR_DB_PATH", os.path.join(tmp_dir, "chroma"))
    monkeypatch.setenv("UPLOAD_DIR", os.path.join(tmp_dir, "uploads"))
    from app.core.config import get_settings

    get_settings.cache_clear()
    yield tmp_dir
    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture()
def client(tmp_data_dirs):
    if os.path.exists("./test.db"):
        os.remove("./test.db")

    from app.db.session import Base, engine
    from app.main import app

    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")


def register_and_login(client, email="user@example.com", password="StrongPass123"):
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Test User"},
    )
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
