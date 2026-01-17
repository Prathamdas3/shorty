import pytest
import time
from fastapi import Request
from app.core.rate_limit import _rate_limit_storage, _cleanup_old_entries


@pytest.fixture(autouse=True)
def reset_rate_limit_storage():
    """Reset rate limit storage before each test."""
    _rate_limit_storage.clear()
    yield


def test_rate_limit_basic_enforcement(client):
    """Test that rate limit enforces after exceeding allowed requests."""
    for _ in range(5):
        response = client.post("/api/link", json={"link": "https://example.com"})
        assert response.status_code == 200

    response = client.post("/api/link", json={"link": "https://example.com"})
    assert response.status_code == 429


def test_rate_limit_response_format(client):
    """Test that rate limit error response has correct format."""
    for _ in range(5):
        client.post("/api/link", json={"link": "https://example.com"})

    response = client.post("/api/link", json={"link": "https://example.com"})

    assert response.status_code == 429
    data = response.json()
    assert "detail" in data
    assert "error" in data["detail"]
    assert data["detail"]["error"] == "Rate limit exceeded"
    assert "message" in data["detail"]
    assert "retry_after" in data["detail"]
    assert isinstance(data["detail"]["retry_after"], int)
    assert data["detail"]["retry_after"] > 0

    assert "Retry-After" in response.headers
    assert response.headers["Retry-After"] == str(data["detail"]["retry_after"])


def test_rate_limit_isolation_by_ip(client):
    """Test that rate limit is isolated by IP address."""
    for _ in range(5):
        client.post("/api/link", json={"link": "https://example.com"})

    response = client.post("/api/link", json={"link": "https://example.com"})
    assert response.status_code == 429

    response = client.post(
        "/api/link",
        json={"link": "https://example.com"},
        headers={"X-Forwarded-For": "192.168.1.100"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/link",
        json={"link": "https://example.com"},
        headers={"X-Forwarded-For": "10.0.0.1"},
    )
    assert response.status_code == 200

    for _ in range(4):
        client.post(
            "/api/link",
            json={"link": "https://example.com"},
            headers={"X-Forwarded-For": "192.168.1.100"},
        )

    response = client.post(
        "/api/link",
        json={"link": "https://example.com"},
        headers={"X-Forwarded-For": "192.168.1.100"},
    )
    assert response.status_code == 429


def test_rate_limit_time_window_expiration(client):
    """Test that rate limit resets after time window expires."""
    for _ in range(5):
        client.post("/api/link", json={"link": "https://example.com"})

    response = client.post("/api/link", json={"link": "https://example.com"})
    assert response.status_code == 429

    time.sleep(61)

    response = client.post("/api/link", json={"link": "https://example.com"})
    assert response.status_code == 200


def test_rate_limit_cleanup(client):
    """Test that cleanup removes old entries."""
    for _ in range(5):
        client.post(
            "/api/link",
            json={"link": "https://example.com"},
            headers={"X-Forwarded-For": "1.1.1.1"},
        )

    for _ in range(5):
        client.post(
            "/api/link",
            json={"link": "https://example.com"},
            headers={"X-Forwarded-For": "2.2.2.2"},
        )

    initial_count = len(_rate_limit_storage)
    assert initial_count > 0

    _cleanup_old_entries(60)

    time.sleep(61)
    _cleanup_old_entries(60)

    final_count = len(_rate_limit_storage)
    assert final_count == 0


def test_rate_limit_different_endpoints():
    """Test that different endpoints have separate rate limits."""
    from app.core.rate_limit import rate_limit
    from unittest.mock import Mock

    @rate_limit(times=2, seconds=60)
    def endpoint1(request: Request):
        return "ok"

    @rate_limit(times=2, seconds=60)
    def endpoint2(request: Request):
        return "ok"

    mock_request = Mock(spec=Request)
    mock_request.client.host = "127.0.0.1"
    mock_request.headers.get = Mock(return_value=None)

    for _ in range(2):
        endpoint1(mock_request)

    assert endpoint2(mock_request) == "ok"


def test_rate_limit_missing_request_object():
    """Test that rate limit raises error if request object is missing."""
    from app.core.rate_limit import rate_limit

    @rate_limit(times=5, seconds=60)
    def test_func():
        return "ok"

    with pytest.raises(ValueError, match="Request object not found"):
        test_func()


def test_rate_limit_counter_reset_after_cleanup():
    """Test that rate limit counter is properly maintained across cleanup cycles."""
    for _ in range(5):
        _cleanup_old_entries(60)

    assert len(_rate_limit_storage) == 0


def test_rate_limit_with_sync_function(client):
    """Test that rate limiting works correctly with sync decorated functions."""
    from app.core.rate_limit import rate_limit
    from unittest.mock import Mock

    @rate_limit(times=3, seconds=60)
    def sync_endpoint(request: Request):
        return "success"

    mock_request = Mock(spec=Request)
    mock_request.client.host = "127.0.0.1"
    mock_request.headers.get = Mock(return_value=None)

    for _ in range(3):
        assert sync_endpoint(mock_request) == "success"

    with pytest.raises(Exception):
        sync_endpoint(mock_request)


def test_get_identifier_with_x_forwarded_for():
    """Test get_identifier with X-Forwarded-For header."""
    from app.core.rate_limit import get_identifier
    from unittest.mock import Mock

    mock_request = Mock(spec=Request)
    mock_request.headers.get = Mock(return_value="192.168.1.100, 10.0.0.1")
    mock_request.client.host = "127.0.0.1"

    identifier = get_identifier(mock_request)
    assert identifier == "192.168.1.100"


def test_get_identifier_without_x_forwarded_for():
    """Test get_identifier without X-Forwarded-For header."""
    from app.core.rate_limit import get_identifier
    from unittest.mock import Mock

    mock_request = Mock(spec=Request)
    mock_request.headers.get = Mock(return_value=None)
    mock_request.client.host = "127.0.0.1"

    identifier = get_identifier(mock_request)
    assert identifier == "127.0.0.1"


def test_get_identifier_with_unknown_client():
    """Test get_identifier when client is None."""
    from app.core.rate_limit import get_identifier
    from unittest.mock import Mock

    mock_request = Mock(spec=Request)
    mock_request.headers.get = Mock(return_value=None)
    mock_request.client = None

    identifier = get_identifier(mock_request)
    assert identifier == "unknown"


def test_rate_limit_storage_isolation():
    """Test that rate limit storage is isolated between different clients."""
    from app.core.rate_limit import rate_limit
    from unittest.mock import Mock

    @rate_limit(times=2, seconds=60)
    def limited_endpoint(request: Request):
        return "success"

    mock_request1 = Mock(spec=Request)
    mock_request1.client.host = "127.0.0.1"
    mock_request1.headers.get = Mock(return_value=None)

    mock_request2 = Mock(spec=Request)
    mock_request2.client.host = "192.168.1.1"
    mock_request2.headers.get = Mock(return_value=None)

    for _ in range(2):
        limited_endpoint(mock_request1)

    with pytest.raises(Exception):
        limited_endpoint(mock_request1)

    assert limited_endpoint(mock_request2) == "success"


def test_rate_limit_multiple_decorated_functions():
    """Test that multiple functions can be decorated with rate_limit independently."""
    from app.core.rate_limit import rate_limit
    from unittest.mock import Mock

    @rate_limit(times=2, seconds=60)
    def endpoint_a(request: Request):
        return "a"

    @rate_limit(times=2, seconds=60)
    def endpoint_b(request: Request):
        return "b"

    mock_request = Mock(spec=Request)
    mock_request.client.host = "127.0.0.1"
    mock_request.headers.get = Mock(return_value=None)

    for _ in range(2):
        assert endpoint_a(mock_request) == "a"

    with pytest.raises(Exception):
        endpoint_a(mock_request)

    assert endpoint_b(mock_request) == "b"


def test_rate_limit_exception_handling():
    """Test that exceptions in decorated function are properly propagated."""
    from app.core.rate_limit import rate_limit
    from unittest.mock import Mock

    @rate_limit(times=5, seconds=60)
    def failing_endpoint(request: Request):
        raise ValueError("Test error")

    mock_request = Mock(spec=Request)
    mock_request.client.host = "127.0.0.1"
    mock_request.headers.get = Mock(return_value=None)

    with pytest.raises(ValueError, match="Test error"):
        failing_endpoint(mock_request)
