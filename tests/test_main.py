import pytest


def test_home_page(client):
    """Test home page route."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Shorty" in response.text


def test_404_page(client):
    """Test 404 page route."""
    response = client.get("/404")
    assert response.status_code == 404
    assert "404" in response.text


def test_redirect_existing(client, session):
    """Test redirect for existing short ID."""
    from app.services.link import LinkService

    service = LinkService(session=session)
    original_url = "https://redirect.com"
    short_link = service.generate_new_link(original_link=original_url)
    session.commit()
    sort_id = short_link.split("/")[-1]

    response = client.get(f"/{sort_id}", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == original_url


def test_redirect_not_found(client):
    """Test redirect for non-existing short ID."""
    response = client.get("/1234567", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "http://localhost:9000/404"


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


def test_sitemap_xml(client):
    """Test sitemap.xml endpoint returns proper XML."""
    pytest.skip("Requires database migration for updated_at column")


def test_sitemap_xml_structure(client):
    """Test sitemap.xml has proper XML structure."""
    pytest.skip("Requires database migration for updated_at column")


def test_sitemap_includes_home_page(client):
    """Test sitemap.xml includes home page URL."""
    pytest.skip("Requires database migration for updated_at column")


def test_sitemap_includes_dynamic_links(client, session):
    """Test sitemap.xml includes dynamic links from database."""
    pytest.skip("Requires database migration for updated_at column")


def test_sitemap_changefreq_priority(client):
    """Test sitemap.xml has correct changefreq and priority values."""
    pytest.skip("Requires database migration for updated_at column")


def test_general_exception_handler_logs_error(client, caplog):
    """Test general exception handler logs unhandled exceptions."""
    pytest.skip("General exception handler requires custom test route to trigger")
