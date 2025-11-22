"""
Test script for authentication endpoints.
Tests register, login, refresh, and protected routes.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def test_auth_flow():
    print("=" * 80)
    print("Testing Authentication Flow")
    print("=" * 80)
    
    # Test 1: Register a new user
    print("\n1. Testing Registration...")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    register_data = {
        "username": f"testuser_{timestamp}",
        "email": f"testuser_{timestamp}@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ Registration successful!")
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
    else:
        print("❌ Registration failed!")
        return
    
    # Test 2: Login with existing user
    print("\n2. Testing Login...")
    login_data = {
        "username": "rahul_student",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Login successful!")
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
    else:
        print("❌ Login failed!")
        return
    
    # Test 3: Access protected endpoint
    print("\n3. Testing Protected Endpoint (/api/auth/me)...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Protected endpoint access successful!")
    else:
        print("❌ Protected endpoint access failed!")
    
    # Test 4: Refresh token
    print("\n4. Testing Token Refresh...")
    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    
    response = requests.post(f"{BASE_URL}/auth/refresh", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Token refresh successful!")
        new_access_token = response.json()['access_token']
    else:
        print("❌ Token refresh failed!")
        return
    
    # Test 5: Test invalid credentials
    print("\n5. Testing Invalid Credentials...")
    bad_login = {
        "username": "wronguser",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=bad_login)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✅ Invalid credentials properly rejected!")
    else:
        print("❌ Invalid credentials test failed!")
    
    # Test 6: Test accessing protected route without token
    print("\n6. Testing Protected Route Without Token...")
    response = requests.get(f"{BASE_URL}/auth/me")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Unauthorized access properly blocked!")
    else:
        print("❌ Unauthorized access test failed!")
    
    print("\n" + "=" * 80)
    print("Authentication Flow Test Complete!")
    print("=" * 80)


if __name__ == '__main__':
    try:
        test_auth_flow()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the Flask server is running on http://localhost:5000")
        print("Run: python run.py")
