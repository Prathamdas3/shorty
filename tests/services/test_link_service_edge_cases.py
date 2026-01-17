"""Tests for LinkService error handling and edge cases."""

import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.services.link import LinkService
from app.core.exception import DbException, AppException
from app.db.schema import Links
from unittest.mock import Mock, patch


def test_link_service_commit_failure(session):
    """Test LinkService handles commit failures."""
    service = LinkService(session=session)

    with patch.object(
        session, "commit", side_effect=IntegrityError("Unique constraint failed")
    ):
        with pytest.raises(DbException) as exc_info:
            service._commit()
        assert "Database operation failed" in str(exc_info.value)


def test_link_service_sqlalchemy_error(session):
    """Test LinkService handles generic SQLAlchemy errors."""
    service = LinkService(session=session)

    with patch.object(
        session, "commit", side_effect=SQLAlchemyError("Connection error")
    ):
        with pytest.raises(DbException) as exc_info:
            service._commit()
        assert "Database operation failed" in str(exc_info.value)


def test_link_service_create_unique_id_length(session):
    """Test _create_unique_id generates correct length."""
    service = LinkService(session=session)

    id_length_7 = service._create_unique_id(7)
    assert len(id_length_7) == 7

    id_length_10 = service._create_unique_id(10)
    assert len(id_length_10) == 10

    id_length_5 = service._create_unique_id(5)
    assert len(id_length_5) == 5


def test_link_service_create_unique_id_uniqueness(session):
    """Test _create_unique_id generates unique IDs."""
    service = LinkService(session=session)

    ids = set()
    for _ in range(100):
        new_id = service._create_unique_id()
        ids.add(new_id)

    assert len(ids) == 100


def test_link_service_generate_new_link_success(session):
    """Test generate_new_link creates link successfully."""
    service = LinkService(session=session)

    short_link = service.generate_new_link("https://example.com")

    assert short_link is not None
    assert "/" in short_link
    assert len(short_link) > 7


def test_link_service_generate_new_link_database_error(session):
    """Test generate_new_link handles database errors."""
    service = LinkService(session=session)

    with patch.object(session, "add", side_effect=IntegrityError("Insert failed")):
        with pytest.raises(DbException):
            service.generate_new_link("https://example.com")


def test_link_service_generate_new_link_exception(session):
    """Test generate_new_link handles general exceptions."""
    service = LinkService(session=session)

    with patch.object(session, "refresh", side_effect=Exception("Refresh failed")):
        with pytest.raises(AppException) as exc_info:
            service.generate_new_link("https://example.com")
        assert "Failed to generate a new link" in str(exc_info.value)


def test_link_service_get_original_link_increments_clicks(session):
    """Test get_original_link increments click count."""
    from app.services.link import LinkService

    service = LinkService(session=session)

    short_link = service.generate_new_link("https://example.com")
    session.commit()
    sort_id = short_link.split("/")[-1]

    from sqlmodel import select

    statement = select(Links).where(Links.sort_id == sort_id)
    link = session.exec(statement).one()

    initial_clicks = link.clicks
    service.get_original_link(sort_id)
    session.commit()

    link = session.exec(statement).one()
    assert link.clicks == initial_clicks + 1


def test_link_service_get_original_link_updates_timestamp(session):
    """Test get_original_link updates last_accessed_at."""
    from app.services.link import LinkService

    service = LinkService(session=session)

    short_link = service.generate_new_link("https://example.com")
    session.commit()
    sort_id = short_link.split("/")[-1]

    from sqlmodel import select
    from datetime import datetime, timedelta
    import time

    time.sleep(0.1)

    service.get_original_link(sort_id)
    session.commit()

    statement = select(Links).where(Links.sort_id == sort_id)
    link = session.exec(statement).one()

    assert link.last_accessed_at is not None


def test_link_service_get_original_link_not_found(session):
    """Test get_original_link returns 404 URL for non-existent ID."""
    service = LinkService(session=session)

    result = service.get_original_link("nonexist")

    assert "404" in result


def test_link_service_get_original_link_database_error(session):
    """Test get_original_link handles database errors."""
    service = LinkService(session=session)

    with patch.object(session, "exec", side_effect=SQLAlchemyError("Query failed")):
        with pytest.raises(AppException) as exc_info:
            service.get_original_link("testid")
        assert "Failed to find the original link" in str(exc_info.value)


def test_link_service_multiple_links_same_url(session):
    """Test generating multiple links for same URL."""
    service = LinkService(session=session)

    link1 = service.generate_new_link("https://example.com")
    link2 = service.generate_new_link("https://example.com")
    link3 = service.generate_new_link("https://example.com")

    assert link1 != link2
    assert link2 != link3
    assert link1 != link3


def test_link_service_click_count_increment(session):
    """Test click count increments correctly over multiple accesses."""
    from app.services.link import LinkService

    service = LinkService(session=session)

    short_link = service.generate_new_link("https://example.com")
    session.commit()
    sort_id = short_link.split("/")[-1]

    from sqlmodel import select

    statement = select(Links).where(Links.sort_id == sort_id)

    for i in range(5):
        service.get_original_link(sort_id)
        session.commit()

    link = session.exec(statement).one()
    assert link.clicks == 5


def test_link_service_id_characters(session):
    """Test _create_unique_id uses correct character set."""
    service = LinkService(session=session)

    test_id = service._create_unique_id(100)

    import string

    valid_chars = string.ascii_letters + string.digits
    assert all(c in valid_chars for c in test_id)
