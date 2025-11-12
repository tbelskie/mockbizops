"""Basic API tests."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_redirect():
    """Test root redirects to docs."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/docs" in response.headers["location"]


def test_customers_without_auth():
    """Test that customers endpoint requires authentication."""
    response = client.get("/api/v1/customers")
    assert response.status_code == 401


def test_customers_with_invalid_key():
    """Test that invalid API key is rejected."""
    response = client.get(
        "/api/v1/customers",
        headers={"X-API-Key": "invalid-key"}
    )
    assert response.status_code == 401


# Add more tests as needed
