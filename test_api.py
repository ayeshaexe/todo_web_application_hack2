#!/usr/bin/env python3
"""
Test script to verify the complete auth flow
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8080"

def test_signup():
    print("Testing signup...")
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        print(f"Signup response: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Signup successful: {result['success']}")
            return result['token']
        else:
            print(f"Signup failed: {response.text}")
            return None
    except Exception as e:
        print(f"Error during signup: {e}")
        return None

def test_login():
    print("\nTesting login...")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Login successful: {result['success']}")
            return result['token']
        else:
            print(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"Error during login: {e}")
        return None

def test_logout(token):
    print("\nTesting logout...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/api/auth/logout", headers=headers)
        print(f"Logout response: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Logout successful: {result['success']}")
            return True
        else:
            print(f"Logout failed: {response.text}")
            return False
    except Exception as e:
        print(f"Error during logout: {e}")
        return False

def test_health():
    print("\nTesting health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check response: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Health check: {result['status']}")
            return True
        else:
            print(f"Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"Error during health check: {e}")
        return False

def test_todos_without_auth():
    print("\nTesting todos endpoint without auth (should fail)...")
    try:
        response = requests.get(f"{BASE_URL}/api/todos")
        print(f"Todos response: {response.status_code}")
        if response.status_code == 401:
            print("Correctly rejected unauthorized request")
            return True
        else:
            print(f"Unexpected response: {response.text}")
            return False
    except Exception as e:
        print(f"Error during todos test: {e}")
        return False

if __name__ == "__main__":
    print("Starting API tests...\n")

    # Test health check first
    test_health()

    # Test signup
    token = test_signup()

    # If signup failed, try login (in case user already exists)
    if not token:
        print("Signup failed, trying login...")
        token = test_login()

    # Test protected endpoints if we have a token
    if token:
        print(f"\nGot token: {token[:20]}...")
        test_logout(token)
    else:
        print("Could not get authentication token")

    # Test unauthorized access
    test_todos_without_auth()

    print("\nTests completed!")