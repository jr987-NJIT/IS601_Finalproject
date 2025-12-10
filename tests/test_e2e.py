"""
Playwright E2E Tests (DEPRECATED)

These Playwright tests have been replaced with simpler REST API E2E tests in test_e2e_manual.py

The Playwright approach was problematic because:
- Browser initialization takes too long
- Requires complex setup and teardown
- Often times out on CI/CD systems
- Tests hang when server is unavailable

For E2E testing, use test_e2e_manual.py which tests the API layer directly.
This is faster, more reliable, and easier to maintain.

To run E2E tests:
1. Start server: uvicorn app.main:app --host 0.0.0.0 --port 8000
2. Run: pytest tests/test_e2e_manual.py -v
"""

import pytest

# Skip all tests in this file
pytestmark = pytest.mark.skip(reason="Use test_e2e_manual.py instead. See docstring for details.")

def test_placeholder_e2e():
    """Placeholder test."""
    pass
