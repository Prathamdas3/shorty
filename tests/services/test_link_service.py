import pytest
from app.services.link import LinkService
from app.db.schema import Links
from sqlmodel import select


def test_generate_new_link(session):
    """Test generating a new short link."""
    service = LinkService(session=session)
    original_url = "https://example.com"
    short_link = service.generate_new_link(original_link=original_url)

    assert short_link.startswith("http://localhost:9000/")
    sort_id = short_link.split("/")[-1]
    assert len(sort_id) == 7

    # Verify in database
    statement = select(Links).where(Links.sort_id == sort_id)
    link = session.exec(statement).one()
    assert link.original_url == original_url
    assert link.clicks == 0


def test_get_original_link_existing(session):
    """Test retrieving an existing original URL and incrementing clicks."""
    service = LinkService(session=session)
    original_url = "https://test.com"
    short_link = service.generate_new_link(original_link=original_url)
    sort_id = short_link.split("/")[-1]

    retrieved_url = service.get_original_link(sort_id=sort_id)
    assert retrieved_url == original_url

    # Verify clicks incremented and timestamp updated
    statement = select(Links).where(Links.sort_id == sort_id)
    link = session.exec(statement).one()
    assert link.clicks == 1
    assert link.last_accessed_at is not None


def test_get_original_link_not_found(session):
    """Test retrieving a non-existing short ID returns 404 URL."""
    service = LinkService(session=session)
    retrieved_url = service.get_original_link(sort_id="nonexist")
    assert retrieved_url == "http://localhost:9000/404"
