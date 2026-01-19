"""Additional tests to improve code coverage."""

import pytest
import time
from unittest.mock import patch, MagicMock
from fastapi import Request, HTTPException
from app.core.rate_limit import _rate_limit_storage, _cleanup_old_entries, rate_limit


def test_cleanup_old_entries_with_old_timestamps():
    """Test _cleanup_old_entries removes entries with old timestamps."""
    now = 1000000.0
    _rate_limit_storage["test_function:key1"] = [now - 100, now - 90]

    _cleanup_old_entries(150)

    # Should be removed since all timestamps are old
    assert "test_function:key1" not in _rate_limit_storage


def test_cleanup_old_entries_mixed():
    """Test _cleanup_old_entries handles mixed old/new timestamps."""
    now = 1000000.0
    _rate_limit_storage["test_func:key1"] = [now - 100, now - 50, now]

    _cleanup_old_entries(60)

    # Should keep 2 recent timestamps (now - 50 and now are within 60 seconds)
    assert len(_rate_limit_storage["test_func:key1"]) == 2


def test_cleanup_old_entries_preserves_valid():
    """Test _cleanup_old_entries preserves valid timestamps."""
    now = 1000000.0
    _rate_limit_storage["test_func:key1"] = [now - 10, now - 5, now]

    _cleanup_old_entries(30)

    # Should keep all 3 timestamps
    assert len(_rate_limit_storage["test_func:key1"]) == 3


def test_cleanup_old_entries_edge_case():
    """Test _cleanup_old_entries with edge case timestamp."""
    now = 1000000.0
    _rate_limit_storage["test_func:key1"] = [now - 60, now - 59.9]

    _cleanup_old_entries(60)

    # Should keep 1 timestamp that's just within the window
    assert len(_rate_limit_storage["test_func:key1"]) == 1


def test_rate_limit_decorator_within_limit():
    """Test rate_limit decorator allows calls within limit."""
    _rate_limit_storage.clear()

    @rate_limit(times=3, seconds=10)
    def test_func(request):
        return "success"

    # Create mock request
    mock_request = MagicMock(spec=Request)
    mock_request.client.host = "127.0.0.1"
    mock_request.headers = {}

    # Should allow 3 calls
    for i in range(3):
        result = test_func(mock_request)
        assert result == "success"


def test_rate_limit_decorator_exceeds_limit():
    """Test rate_limit decorator blocks calls exceeding limit."""
    _rate_limit_storage.clear()

    @rate_limit(times=2, seconds=10)
    def test_func(request):
        return "success"

    # Create mock request
    mock_request = MagicMock(spec=Request)
    mock_request.client.host = "127.0.0.1"
    mock_request.headers = {}

    # Make 2 allowed calls
    test_func(mock_request)
    test_func(mock_request)

    # Third call should raise exception
    with pytest.raises(HTTPException) as exc_info:
        test_func(mock_request)

    assert exc_info.value.status_code == 429
    assert "Rate limit exceeded" in str(exc_info.value.detail)


def test_rate_limit_decorator_no_request():
    """Test rate_limit decorator fails without Request object."""
    _rate_limit_storage.clear()

    @rate_limit(times=1, seconds=10)
    def test_func():
        return "success"

    # Should fail without request
    with pytest.raises(ValueError) as exc_info:
        test_func()

    assert "Request object not found" in str(exc_info.value)
