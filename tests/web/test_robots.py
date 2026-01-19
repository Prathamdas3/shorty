import pytest


def test_robots_txt(client):
    """Test robots.txt endpoint returns proper content."""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert "Cache-Control" in response.headers
    assert "public" in response.headers["Cache-Control"]
    assert "86400" in response.headers["Cache-Control"]


def test_robots_txt_content(client):
    """Test robots.txt content includes expected directives."""
    response = client.get("/robots.txt")
    content = response.text

    assert "User-agent: Googlebot" in content
    assert "Allow: /" in content
    assert "User-agent: Bingbot" in content
    assert "User-agent: GPTBot" in content
    assert "User-agent: ChatGPT-User" in content
    assert "User-agent: Claude-Web" in content
    assert "User-agent: CCBot" in content
    assert "User-agent: PerplexityBot" in content
    assert "Disallow: /api/" in content
    assert "Disallow: /docs" in content
    assert "Disallow: /admin/" in content
    assert "Disallow: /logs/" in content
    assert "Sitemap:" in content


def test_robots_txt_no_sensitive_areas(client):
    """Test robots.txt blocks sensitive areas."""
    response = client.get("/robots.txt")
    content = response.text

    # Ensure sensitive areas are disallowed
    assert "Disallow: /api/" in content
    assert "Disallow: /docs" in content
    assert "Disallow: /admin/" in content
    assert "Disallow: /logs/" in content


def test_robots_txt_allows_ai_crawlers(client):
    """Test robots.txt allows AI crawlers for training."""
    response = client.get("/robots.txt")
    content = response.text

    # Check AI crawlers are allowed
    assert "User-agent: GPTBot" in content
    assert "User-agent: ChatGPT-User" in content
    assert "User-agent: Claude-Web" in content
    assert "User-agent: PerplexityBot" in content
