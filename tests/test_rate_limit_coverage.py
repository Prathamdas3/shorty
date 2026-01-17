"""Additional tests to improve code coverage."""

import pytest
from app.core.rate_limit import _rate_limit_storage, _cleanup_old_entries


def test_cleanup_old_entries_with_old_timestamps():
    """Test _cleanup_old_entries removes entries with old timestamps."""
    now = 1000000.0
    _rate_limit_storage["test_function:key1"] = [now - 100, now - 90]
    _rate_limit_storage["test_function:key2"] = [now - 200]

    _cleanup_old_entries(150)

    assert "test_function:key2" not in _rate_limit_storage
    assert len(_rate_limit_storage["test_function:key1"]) == 0


def test_cleanup_old_entries_mixed():
    """Test _cleanup_old_entries handles mixed old/new timestamps."""
    now = 1000000.0
    _rate_limit_storage["test_func:key1"] = [now - 100, now - 50, now]

    _cleanup_old_entries(60)

    assert len(_rate_limit_storage["test_func:key1"]) == 2


def test_cleanup_old_entries_removes_empty_keys():
    """Test _cleanup_old_entries removes keys with no timestamps."""
    now = 1000000.0
    _rate_limit_storage["test_func:empty_key"] = [now - 200]

    _cleanup_old_entries(150)

    assert "test_func:empty_key" not in _rate_limit_storage


def test_cleanup_old_entries_multiple_keys():
    """Test _cleanup_old_entries processes multiple keys."""
    now = 1000000.0
    _rate_limit_storage["test_func:key1"] = [now - 100]
    _rate_limit_storage["test_func:key2"] = [now - 150]
    _rate_limit_storage["test_func:key3"] = [now - 200]

    _cleanup_old_entries(120)

    assert "test_func:key3" not in _rate_limit_storage


def test_cleanup_old_entries_preserves_valid():
    """Test _cleanup_old_entries preserves valid timestamps."""
    now = 1000000.0
    _rate_limit_storage["test_func:key1"] = [now - 10, now - 5, now]

    _cleanup_old_entries(30)

    assert len(_rate_limit_storage["test_func:key1"]) == 3


def test_cleanup_old_entries_edge_case():
    """Test _cleanup_old_entries with edge case timestamp."""
    now = 1000000.0
    _rate_limit_storage["test_func:key1"] = [now - 60, now - 59.9]

    _cleanup_old_entries(60)

    assert len(_rate_limit_storage["test_func:key1"]) == 1


def test_rate_limit_storage_manipulation():
    """Test direct manipulation of rate limit storage."""
    _rate_limit_storage["test_key"] = [1000.0, 1001.0]
    assert len(_rate_limit_storage["test_key"]) == 2


def test_cleanup_empty_storage():
    """Test cleanup with empty storage."""
    _rate_limit_storage.clear()
    _cleanup_old_entries(60)

    assert len(_rate_limit_storage) == 0


def test_cleanup_very_old_entries():
    """Test cleanup with very old entries."""
    now = 1000000.0
    _rate_limit_storage["test_func:old_key"] = [now - 10000, now - 5000]

    _cleanup_old_entries(1000)

    assert "test_func:old_key" not in _rate_limit_storage
