import pytest
from app.core.exception import AppException, LinkNotFound, DbException


def test_app_exception():
    """Test AppException can be raised."""
    with pytest.raises(AppException):
        raise AppException("test")


def test_link_not_found():
    """Test LinkNotFound can be raised."""
    with pytest.raises(LinkNotFound):
        raise LinkNotFound("not found")


def test_db_exception():
    """Test DbException can be raised."""
    with pytest.raises(DbException):
        raise DbException("db error")
