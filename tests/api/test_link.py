import pytest
from app.db.schema import Links
from sqlmodel import select


def test_create_short_link(client, session):
    """Test creating a short link via API."""
    response = client.post("/api/link", json={"link": "https://example.com"})
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert "link" in data["data"]
    assert "qr" in data["data"]

    # Verify in database
    short_link = data["data"]["link"]
    sort_id = short_link.split("/")[-1]
    statement = select(Links).where(Links.sort_id == sort_id)
    link = session.exec(statement).one()
    assert link.original_url == "https://example.com/"


def test_create_short_link_invalid_url(client):
    """Test creating short link with invalid URL."""
    response = client.post("/api/link", json={"link": "invalid-url"})
    assert response.status_code == 422


def test_create_short_link_localhost(client):
    """Test creating short link with localhost URL."""
    response = client.post("/api/link", json={"link": "http://localhost"})
    assert response.status_code == 422
