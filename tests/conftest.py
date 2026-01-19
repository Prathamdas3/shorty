import pytest
import tempfile
import os
from sqlmodel import create_engine, Session, SQLModel
from fastapi.testclient import TestClient
from app.main import app
from app.db.init import get_session
from app.db.schema import Links  # Import to register models
import app.core.config as config_module


@pytest.fixture(scope="session")
def engine():
    """Create temporary SQLite engine for tests."""
    db_file = tempfile.NamedTemporaryFile(delete=False)
    db_file.close()
    engine = create_engine(f"sqlite:///{db_file.name}", echo=False)
    SQLModel.metadata.create_all(engine)
    yield engine
    os.unlink(db_file.name)


@pytest.fixture(scope="function")
def session(engine):
    """Provide a test database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def client(session):
    """Provide FastAPI TestClient with overridden session dependency."""
    # Override config attributes for tests
    original_frontend_url = config_module.config.frontend_url
    original_site_url = config_module.config.site_url

    config_module.config.frontend_url = "http://testserver"
    config_module.config.site_url = "http://testserver"

    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app) as client:
        yield client

    # Restore original config
    config_module.config.frontend_url = original_frontend_url
    config_module.config.site_url = original_site_url
