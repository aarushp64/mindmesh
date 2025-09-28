import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import Base, get_db
from backend.main import app

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_note(client):
    response = client.post(
        "/notes",
        json={
            "title": "Test Note",
            "content": "This is a test note",
            "link_ids": [],
            "tags": ["test"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note"
    assert data["tags"] == ["test"]
    assert "id" in data
    assert data["layer"] == "factual"

def test_list_notes(client):
    # Create a test note first
    client.post(
        "/notes",
        json={
            "title": "Test Note",
            "content": "This is a test note",
            "link_ids": [],
            "tags": ["test"]
        }
    )
    
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)
    assert all(isinstance(note, dict) for note in data)

def test_delete_note(client):
    # Create a note to delete
    create_response = client.post(
        "/notes",
        json={
            "title": "Test Note",
            "content": "This is a test note",
            "link_ids": [],
            "tags": ["test"]
        }
    )
    note_id = create_response.json()["id"]
    
    # Delete the note
    delete_response = client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"ok": True}
    
    # Verify note is deleted
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404