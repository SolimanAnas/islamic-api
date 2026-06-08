import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client():
    """Create a test client that shares data across all tests."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def loaded_store():
    """Ensure data is loaded before tests run."""
    from app.services.data_loader import get_store
    return get_store()
