"""
Tests for the main FastAPI application.
"""

from fastapi.testclient import TestClient

from happenings.main import app

client = TestClient(app)


def test_hello_world():
    """Test the hello world endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
