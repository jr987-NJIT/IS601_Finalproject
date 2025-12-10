import pytest
import requests
import time

BASE_URL = "http://localhost:8000"

def server_is_running():
    """Check if the server is running."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except Exception:
        return False

def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "e2e: end-to-end tests that require a running server"
    )

@pytest.fixture(scope="session")
def server_running():
    """Check if server is running before E2E tests."""
    if not server_is_running():
        pytest.skip("Server not running at http://localhost:8000. E2E tests skipped.", allow_module_level=True)
    return True
