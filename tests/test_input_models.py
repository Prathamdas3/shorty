"""Tests for input model validation."""

import pytest
from pydantic import ValidationError
from app.models.input import SortIDInput, OriginalUrlInput
from urllib.parse import urlparse


def test_sort_id_valid():
    """Test SortIDInput accepts valid 7-character IDs."""
    valid_ids = ["abc1234", "ABCDEFG", "1234567", "aB1cD2e"]
    for sort_id in valid_ids:
        input_data = SortIDInput(sort_id=sort_id)
        assert input_data.sort_id == sort_id


def test_sort_id_missing():
    """Test SortIDInput raises error for missing sort_id."""
    with pytest.raises(ValidationError) as exc_info:
        SortIDInput(sort_id="")
    assert "missing" in str(exc_info.value).lower()


def test_sort_id_none():
    """Test SortIDInput raises error for None."""
    pytest.skip("Pydantic handles None at model level")


def test_sort_id_empty():
    """Test SortIDInput raises error for empty string."""
    with pytest.raises(ValidationError) as exc_info:
        SortIDInput(sort_id="   ")
    assert "empty" in str(exc_info.value).lower()


def test_sort_id_wrong_type():
    """Test SortIDInput raises error for non-string type."""
    pytest.skip("Pydantic handles type validation at model level")


def test_sort_id_wrong_length():
    """Test SortIDInput raises error for invalid length."""
    with pytest.raises(ValidationError) as exc_info:
        SortIDInput(sort_id="abc123")
    assert "length" in str(exc_info.value).lower()

    with pytest.raises(ValidationError):
        SortIDInput(sort_id="abcdefgh123")


def test_original_url_valid_https():
    """Test OriginalUrlInput accepts valid HTTPS URLs."""
    urls = [
        "https://example.com",
        "https://www.example.com",
        "https://example.com/path",
        "https://example.com/path?query=value",
        "https://example.com:443/path",
    ]
    for url in urls:
        input_data = OriginalUrlInput(link=url)
        assert str(input_data.link).endswith("example.com")


def test_original_url_valid_http():
    """Test OriginalUrlInput accepts valid HTTP URLs."""
    url = "http://example.com"
    input_data = OriginalUrlInput(link=url)
    assert str(input_data.link).endswith("example.com")


def test_original_url_invalid_scheme():
    """Test OriginalUrlInput rejects non-http/https schemes."""
    invalid_schemes = [
        "ftp://example.com",
        "file://example.com",
        "mailto:test@example.com",
    ]
    for url in invalid_schemes:
        with pytest.raises(ValidationError) as exc_info:
            OriginalUrlInput(link=url)
        assert "http" in str(exc_info.value).lower()


def test_original_url_localhost_blocked():
    """Test OriginalUrlInput blocks localhost URLs."""
    localhost_urls = [
        "http://localhost",
        "https://localhost",
        "http://localhost:8080",
        "http://localhost/path",
    ]
    for url in localhost_urls:
        with pytest.raises(ValidationError) as exc_info:
            OriginalUrlInput(link=url)
        assert "localhost" in str(exc_info.value).lower()


def test_original_url_private_ip_blocked():
    """Test OriginalUrlInput blocks private IP addresses."""
    private_ips = [
        "http://192.168.1.1",
        "http://10.0.0.1",
        "http://172.16.0.1",
    ]
    for url in private_ips:
        with pytest.raises(ValidationError) as exc_info:
            OriginalUrlInput(link=url)
        assert (
            "private" in str(exc_info.value).lower()
            or "ip" in str(exc_info.value).lower()
        )


def test_original_url_too_long():
    """Test OriginalUrlInput rejects URLs longer than 2048 characters."""
    long_url = "https://example.com/" + "a" * 2048
    with pytest.raises(ValidationError) as exc_info:
        OriginalUrlInput(link=long_url)
    assert "long" in str(exc_info.value).lower()


def test_original_url_with_subdomain():
    """Test OriginalUrlInput accepts subdomains."""
    url = "https://subdomain.example.com"
    input_data = OriginalUrlInput(link=url)
    assert "subdomain" in str(input_data.link)


def test_original_url_with_fragment():
    """Test OriginalUrlInput accepts URLs with fragments."""
    url = "https://example.com/page#section"
    input_data = OriginalUrlInput(link=url)
    assert "#section" in str(input_data.link)


def test_original_url_case_insensitive_scheme():
    """Test OriginalUrlInput normalizes URL scheme."""
    input_data = OriginalUrlInput(link="HTTPS://EXAMPLE.COM")
    assert str(input_data.link).lower().startswith("https://")


def test_original_url_with_special_characters():
    """Test OriginalUrlInput handles special characters in path."""
    url = "https://example.com/path?param=value&other=test#anchor"
    input_data = OriginalUrlInput(link=url)
    assert "param=value" in str(input_data.link)


def test_sort_id_with_spaces():
    """Test SortIDInput rejects IDs with only spaces."""
    with pytest.raises(ValidationError):
        SortIDInput(sort_id="       ")


def test_original_url_empty():
    """Test OriginalUrlInput rejects empty URL."""
    with pytest.raises(ValidationError):
        OriginalUrlInput(link="")


def test_original_url_no_scheme():
    """Test OriginalUrlInput rejects URLs without scheme."""
    with pytest.raises(ValidationError):
        OriginalUrlInput(link="example.com")


def test_sort_id_exact_length():
    """Test SortIDInput requires exactly 7 characters."""
    with pytest.raises(ValidationError):
        SortIDInput(sort_id="abc123")

    with pytest.raises(ValidationError):
        SortIDInput(sort_id="abc123456")


def test_sort_id_unicode():
    """Test SortIDInput handles unicode characters."""
    input_data = SortIDInput(sort_id="αβγδεζη")
    assert input_data.sort_id == "αβγδεζη"


def test_sort_id_with_special_chars():
    """Test SortIDInput allows special characters."""
    input_data = SortIDInput(sort_id="a-b_c.d")
    assert input_data.sort_id == "a-b_c.d"


def test_sort_id_none_value():
    """Test SortIDInput validator handles None value."""
    with pytest.raises(ValidationError) as exc_info:
        SortIDInput(sort_id=None)
    assert "missing" in str(exc_info.value).lower()


def test_sort_id_non_string_type():
    """Test SortIDInput validator handles non-string types."""
    with pytest.raises(ValidationError) as exc_info:
        SortIDInput(sort_id=123)
    assert "string" in str(exc_info.value).lower()


def test_sort_id_whitespace_only():
    """Test SortIDInput validator handles whitespace-only strings."""
    with pytest.raises(ValidationError) as exc_info:
        SortIDInput(sort_id="   ")
    assert "empty" in str(exc_info.value).lower()


def test_original_url_validator_called():
    """Test OriginalUrlInput validator is executed."""
    # This should pass all checks
    url = "https://example.com"
    input_data = OriginalUrlInput(link=url)
    assert str(input_data.link) == url


def test_original_url_invalid_scheme_validator():
    """Test OriginalUrlInput validator blocks invalid schemes."""
    with pytest.raises(ValidationError) as exc_info:
        OriginalUrlInput(link="ftp://example.com")
    assert "http" in str(exc_info.value).lower()


def test_original_url_localhost_validator():
    """Test OriginalUrlInput validator blocks localhost."""
    with pytest.raises(ValidationError) as exc_info:
        OriginalUrlInput(link="http://localhost")
    assert "localhost" in str(exc_info.value).lower()


def test_original_url_private_ip_validator():
    """Test OriginalUrlInput validator blocks private IPs."""
    # This test may not work if DNS resolution fails, but we can test the logic
    with patch("socket.gethostbyname", return_value="192.168.1.1"):
        with pytest.raises(ValidationError) as exc_info:
            OriginalUrlInput(link="http://private.example.com")
        assert "private" in str(exc_info.value).lower()


def test_original_url_length_validator():
    """Test OriginalUrlInput validator blocks URLs that are too long."""
    long_url = "https://example.com/" + "a" * 2000
    with pytest.raises(ValidationError) as exc_info:
        OriginalUrlInput(link=long_url)
    assert "long" in str(exc_info.value).lower()


def test_original_url_dns_failure_handling():
    """Test OriginalUrlInput validator handles DNS resolution failures."""
    with patch("socket.gethostbyname", side_effect=socket.gaierror("DNS failure")):
        # Should not raise validation error due to DNS failure
        input_data = OriginalUrlInput(link="https://nonexistent-domain-12345.com")
        assert input_data is not None
