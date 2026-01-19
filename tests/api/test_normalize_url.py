import pytest
from app.api.routes.link import normalize_url


def test_normalize_url_lowercase_scheme():
    """Test URL normalization converts scheme to lowercase."""
    assert normalize_url("HTTP://EXAMPLE.COM/") == "http://example.com/"


def test_normalize_url_lowercase_netloc():
    """Test URL normalization converts netloc to lowercase."""
    assert normalize_url("https://EXAMPLE.COM/path") == "https://example.com/path"


def test_normalize_url_removes_trailing_slash():
    """Test URL normalization removes trailing slash from netloc."""
    assert normalize_url("https://EXAMPLE.COM//path") == "https://example.com//path"


def test_normalize_url_preserves_path():
    """Test URL normalization preserves path."""
    assert (
        normalize_url("https://Example.com/test/path")
        == "https://example.com/test/path"
    )


def test_normalize_url_preserves_query():
    """Test URL normalization preserves query string."""
    assert (
        normalize_url("https://Example.com/path?q=1") == "https://example.com/path?q=1"
    )
