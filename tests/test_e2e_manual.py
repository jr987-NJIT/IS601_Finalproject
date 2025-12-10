"""
E2E Tests for IS601 Module 14 Application

These tests are REST API-based E2E tests that verify the complete application flow.
They work with both local and Docker deployments.

For Docker deployment:
  docker-compose up -d
  pytest tests/test_e2e_manual.py -v
  docker-compose down

For local deployment:
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  pytest tests/test_e2e_manual.py -v
"""

import pytest
import requests
import time

BASE_URL = "http://localhost:8000"

@pytest.mark.e2e
def test_server_health():
    """Verify server is healthy."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.e2e
def test_register_user():
    """Test user registration endpoint."""
    user_data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "SecurePass123"
    }
    response = requests.post(f"{BASE_URL}/users/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]

@pytest.mark.e2e
def test_login():
    """Test user login endpoint."""
    # First register
    user_data = {
        "username": f"loginuser_{int(time.time())}",
        "email": f"login_{int(time.time())}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    
    # Then login
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

@pytest.mark.e2e
def test_create_calculation():
    """Test calculation creation."""
    # Register and login
    timestamp = int(time.time())
    user_data = {
        "username": f"calcuser_{timestamp}",
        "email": f"calc_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Create calculation
    headers = {"Authorization": f"Bearer {token}"}
    calc_data = {"a": 10, "b": 5, "type": "Add"}
    response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["result"] == 15

@pytest.mark.e2e
def test_get_calculations():
    """Test retrieving calculations."""
    # Register and login
    timestamp = int(time.time())
    user_data = {
        "username": f"getuser_{timestamp}",
        "email": f"get_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/calculations/", headers=headers)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.e2e
def test_update_profile():
    """Test user profile update."""
    # Register and login
    timestamp = int(time.time())
    user_data = {
        "username": f"profuser_{timestamp}",
        "email": f"prof_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Update profile
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"email": f"newemail_{timestamp}@example.com"}
    response = requests.put(f"{BASE_URL}/users/me", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == update_data["email"]

@pytest.mark.e2e
def test_change_password():
    """Test password change."""
    # Register and login
    timestamp = int(time.time())
    user_data = {
        "username": f"pwduser_{timestamp}",
        "email": f"pwd_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Change password
    headers = {"Authorization": f"Bearer {token}"}
    pwd_data = {
        "current_password": user_data["password"],
        "new_password": "NewSecurePass456"
    }
    response = requests.post(f"{BASE_URL}/users/change-password", json=pwd_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


# ============ Additional Comprehensive E2E Tests ============

@pytest.mark.e2e
def test_division_operation():
    """Test division calculation operation."""
    timestamp = int(time.time())
    user_data = {
        "username": f"divuser_{timestamp}",
        "email": f"div_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    calc_data = {"a": 20, "b": 4, "type": "Divide"}
    response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["result"] == 5.0


@pytest.mark.e2e
def test_multiplication_operation():
    """Test multiplication calculation operation."""
    timestamp = int(time.time())
    user_data = {
        "username": f"multuser_{timestamp}",
        "email": f"mult_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    calc_data = {"a": 7, "b": 8, "type": "Multiply"}
    response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["result"] == 56


@pytest.mark.e2e
def test_subtraction_operation():
    """Test subtraction calculation operation."""
    timestamp = int(time.time())
    user_data = {
        "username": f"subuser_{timestamp}",
        "email": f"sub_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    calc_data = {"a": 50, "b": 20, "type": "Subtract"}
    response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["result"] == 30


@pytest.mark.e2e
def test_division_by_zero_error():
    """Test that division by zero returns error."""
    timestamp = int(time.time())
    user_data = {
        "username": f"zerodiv_{timestamp}",
        "email": f"zerodiv_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    calc_data = {"a": 10, "b": 0, "type": "Divide"}
    response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
    
    # API returns 422 (Unprocessable Entity) for validation errors
    assert response.status_code == 422
    data = response.json()
    assert "Division by zero" in str(data)


@pytest.mark.e2e
def test_get_specific_calculation():
    """Test retrieving a specific calculation by ID."""
    timestamp = int(time.time())
    user_data = {
        "username": f"getspecific_{timestamp}",
        "email": f"getspec_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create calculation
    calc_data = {"a": 15, "b": 3, "type": "Multiply"}
    create_response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
    calc_id = create_response.json()["id"]
    
    # Get specific calculation
    get_response = requests.get(f"{BASE_URL}/calculations/{calc_id}", headers=headers)
    
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == calc_id
    assert data["result"] == 45


@pytest.mark.e2e
def test_update_calculation():
    """Test updating a calculation."""
    timestamp = int(time.time())
    user_data = {
        "username": f"updatecalc_{timestamp}",
        "email": f"updatecalc_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create calculation
    calc_data = {"a": 10, "b": 5, "type": "Add"}
    create_response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
    calc_id = create_response.json()["id"]
    
    # Update calculation
    update_data = {"a": 20, "b": 10, "type": "Subtract"}
    update_response = requests.put(f"{BASE_URL}/calculations/{calc_id}", json=update_data, headers=headers)
    
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["result"] == 10  # 20 - 10


@pytest.mark.e2e
def test_delete_calculation():
    """Test deleting a calculation."""
    timestamp = int(time.time())
    user_data = {
        "username": f"deletecalc_{timestamp}",
        "email": f"deletecalc_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create calculation
    calc_data = {"a": 100, "b": 50, "type": "Add"}
    create_response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
    calc_id = create_response.json()["id"]
    
    # Delete calculation
    delete_response = requests.delete(f"{BASE_URL}/calculations/{calc_id}", headers=headers)
    
    # API returns 204 (No Content) for successful delete operations
    assert delete_response.status_code == 204
    
    # Verify it's deleted
    get_response = requests.get(f"{BASE_URL}/calculations/{calc_id}", headers=headers)
    assert get_response.status_code == 404


@pytest.mark.e2e
def test_duplicate_username_rejected():
    """Test that duplicate username registration is rejected."""
    timestamp = int(time.time())
    username = f"duplicatetest_{timestamp}"
    user_data = {
        "username": username,
        "email": f"dup1_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    
    # First registration should succeed
    response1 = requests.post(f"{BASE_URL}/users/register", json=user_data)
    assert response1.status_code == 201
    
    # Second registration with same username should fail
    user_data["email"] = f"dup2_{timestamp}@example.com"
    response2 = requests.post(f"{BASE_URL}/users/register", json=user_data)
    assert response2.status_code == 400


@pytest.mark.e2e
def test_invalid_login():
    """Test login with invalid credentials fails."""
    response = requests.post(f"{BASE_URL}/users/login", json={
        "username": "nonexistent_user_12345",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401


@pytest.mark.e2e
def test_get_current_user():
    """Test retrieving current user info."""
    timestamp = int(time.time())
    user_data = {
        "username": f"currentuser_{timestamp}",
        "email": f"current_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]


@pytest.mark.e2e
def test_profile_username_change():
    """Test changing username in profile."""
    timestamp = int(time.time())
    old_username = f"oldname_{timestamp}"
    new_username = f"newname_{timestamp}"
    user_data = {
        "username": old_username,
        "email": f"profilechange_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": old_username,
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Update username
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"username": new_username}
    response = requests.put(f"{BASE_URL}/users/me", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == new_username


@pytest.mark.e2e
def test_unauthorized_access_without_token():
    """Test that endpoints require authentication."""
    response = requests.get(f"{BASE_URL}/calculations/")
    
    # API returns 401 (Unauthorized) when authentication token is missing
    assert response.status_code == 401


@pytest.mark.e2e
def test_multiple_calculations_per_user():
    """Test that user can create and manage multiple calculations."""
    timestamp = int(time.time())
    user_data = {
        "username": f"multicalc_{timestamp}",
        "email": f"multicalc_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    requests.post(f"{BASE_URL}/users/register", json=user_data)
    
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create multiple calculations
    calc_ids = []
    for i in range(3):
        calc_data = {"a": i + 1, "b": i + 2, "type": "Add"}
        response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
        assert response.status_code == 201
        calc_ids.append(response.json()["id"])
    
    # Verify all are retrieved
    response = requests.get(f"{BASE_URL}/calculations/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3

