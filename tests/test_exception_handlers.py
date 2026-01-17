import pytest
from unittest.mock import patch, MagicMock
from app.core.exception import (
    LinkNotFound,
    DbException,
    AppException,
)


def test_link_not_found_exception():
    """Test LinkNotFound exception can be raised."""
    with pytest.raises(LinkNotFound, match="Link not found"):
        raise LinkNotFound("Link not found")


def test_link_not_found_exception_empty():
    """Test LinkNotFound with empty message."""
    with pytest.raises(LinkNotFound, match=""):
        raise LinkNotFound("")


def test_db_exception_exception():
    """Test DbException exception can be raised."""
    with pytest.raises(DbException, match="Database connection failed"):
        raise DbException("Database connection failed")


def test_db_exception_with_detailed_message():
    """Test DbException preserves message."""
    exc = DbException("Connection timeout: timeout exceeded")
    assert str(exc) == "Connection timeout: timeout exceeded"


def test_app_exception_exception():
    """Test AppException exception can be raised."""
    with pytest.raises(AppException, match="Application error occurred"):
        raise AppException("Application error occurred")


def test_app_exception_generic():
    """Test AppException with generic error message."""
    with pytest.raises(AppException, match="Something went wrong"):
        raise AppException("Something went wrong")


def test_db_exception_handler_via_api(client, session):
    """Test DbException handler through API endpoint."""
    # Mock LinkService to raise DbException
    with patch("app.api.link.LinkService") as MockLinkService:
        mock_service = MockLinkService.return_value
        mock_service.generate_new_link.side_effect = DbException("Database error")

        response = client.post("/api/link", json={"link": "https://example.com"})

        # Should get 500 error from db_exception_handler
        assert response.status_code == 500
        data = response.json()
        assert "database_error" in data.get("error_type", "")
        assert "try again later" in data.get("detail", "").lower()


def test_app_exception_handler_via_redirect(client):
    """Test AppException handler through redirect endpoint."""
    # Mock LinkService to raise AppException
    from app.services.link import LinkService

    with patch.object(LinkService, "get_original_link") as mock_get:
        mock_get.side_effect = AppException("Failed to find link")

        response = client.get("/1234567", follow_redirects=False)

        # Should get 500 error from app_exception_handler
        assert response.status_code == 500
        data = response.json()
        assert "application_error" in data.get("error_type", "")
