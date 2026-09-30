import os
import tempfile

# File-backed SQLite: an in-memory DB is private to each connection, so tables
# created here were invisible to the TestClient's worker threads.
os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{tempfile.mkdtemp()}/test.db"

from fastapi.testclient import TestClient

from app.db import Base, engine
from app.main import app

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_patient():
    response = client.post("/patients", json={"display_name": "Demo Patient"})
    assert response.status_code == 201
    assert response.json()["display_name"] == "Demo Patient"


def test_missing_patient():
    response = client.get("/patients/not-real")
    assert response.status_code == 404
