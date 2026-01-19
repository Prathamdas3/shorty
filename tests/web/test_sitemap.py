import pytest


def test_sitemap_xml(client):
    """Test sitemap.xml endpoint returns proper XML."""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert "Cache-Control" in response.headers
    assert "public" in response.headers["Cache-Control"]
    assert "86400" in response.headers["Cache-Control"]


def test_sitemap_xml_structure(client):
    """Test sitemap.xml has proper XML structure."""
    response = client.get("/sitemap.xml")
    content = response.text

    assert '<?xml version="1.0" encoding="UTF-8"?>' in content
    assert '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' in content
    assert "</urlset>" in content


def test_sitemap_includes_home_page(client):
    """Test sitemap.xml includes home page URL."""
    response = client.get("/sitemap.xml")
    content = response.text

    # Should include the home page
    assert "<loc>" in content
    assert "<priority>1.0</priority>" in content


def test_sitemap_includes_static_pages(client):
    """Test sitemap.xml includes static pages like about and contact."""
    response = client.get("/sitemap.xml")
    content = response.text

    # Should include about and contact pages
    assert "/about" in content
    assert "/contact" in content


def test_sitemap_changefreq_priority(client):
    """Test sitemap.xml has correct changefreq and priority values."""
    response = client.get("/sitemap.xml")
    content = response.text

    # Check for expected changefreq values
    assert "changefreq" in content
    assert "daily" in content
    assert "monthly" in content

    # Check for priority values
    assert "priority" in content
    assert "1.0" in content
    assert "0.8" in content
    assert "0.7" in content
