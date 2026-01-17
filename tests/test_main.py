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
    session.commit()  # Ensure committed
    sort_id = short_link.split("/")[-1]

    response = client.get(f"/{sort_id}", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == original_url


def test_redirect_not_found(client):
    """Test redirect for non-existing short ID."""
    response = client.get("/1234567", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "http://localhost:9000/404"
