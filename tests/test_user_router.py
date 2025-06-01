"""
Tests for the main FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from happenings.infrastructure.persistence import Base, get_db
from happenings.main import app

# Create a test database
SQLITE_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_signup_return_access_and_refresh_tokens():
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
    }

    response = client.post("/signup", json=signup_data)

    assert response.status_code == 201
    response_data = response.json()

    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert len(response_data["access_token"]) > 0
    assert len(response_data["refresh_token"]) > 0


def test_signup_return_422_when_missing_fields():
    incomplete_data = {
        "username": "testuser",
        "email": "test@example.com",
        # missing password
    }

    response = client.post("/signup", json=incomplete_data)
    assert response.status_code == 422  # Validation error


def test_signup_return_409_when_duplicate_username():
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
    }

    # First signup should succeed
    response1 = client.post("/signup", json=signup_data)
    assert response1.status_code == 201

    # Second signup with same username should fail
    duplicate_data = {
        "username": "testuser",  # Same username
        "email": "different@example.com",
        "password": "anotherpassword",
    }

    response2 = client.post("/signup", json=duplicate_data)
    assert response2.status_code == 409  # Conflict
    assert "detail" in response2.json()


def test_signup_return_409_when_duplicate_email():
    signup_data = {
        "username": "testuser1",
        "email": "test@example.com",
        "password": "securepassword123",
    }

    # First signup should succeed
    response1 = client.post("/signup", json=signup_data)
    assert response1.status_code == 201

    # Second signup with same email should fail
    duplicate_data = {
        "username": "testuser2",
        "email": "test@example.com",  # Same email
        "password": "anotherpassword",
    }

    response2 = client.post("/signup", json=duplicate_data)
    assert response2.status_code == 409  # Conflict
    assert "detail" in response2.json()


def test_login_return_access_and_refresh_tokens():
    # First create a user
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
    }
    signup_response = client.post("/signup", json=signup_data)
    assert signup_response.status_code == 201

    # Then try to login
    login_data = {"username": "testuser", "password": "securepassword123"}

    response = client.post("/login", json=login_data)
    assert response.status_code == 200

    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert len(response_data["access_token"]) > 0
    assert len(response_data["refresh_token"]) > 0


def test_login_return_401_when_invalid_credentials():
    login_data = {"username": "nonexistent", "password": "wrongpassword"}

    response = client.post("/login", json=login_data)
    assert response.status_code == 401
    assert "detail" in response.json()
