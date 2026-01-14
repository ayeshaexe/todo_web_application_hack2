#!/usr/bin/env python3
"""
Test script to simulate the exact API response format
"""
import json
from datetime import datetime, timezone
from models import Todo
from schemas import TodoResponse
from user_models import User, UserPublic, AuthResponse
from pydantic import BaseModel

def test_todo_response_serialization():
    """Test TodoResponse serialization like the API would return"""
    print("Testing TodoResponse serialization...")

    # Create a mock todo object similar to what comes from the database
    mock_todo = Todo(
        id=1,
        user_id="test-user-id",
        title="Test Todo",
        description="Test Description",
        completed=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    # Create TodoResponse like the API endpoint would
    try:
        response = TodoResponse(
            id=mock_todo.id,
            user_id=mock_todo.user_id,
            title=mock_todo.title,
            description=mock_todo.description,
            completed=mock_todo.completed,
            created_at=mock_todo.created_at,
            updated_at=mock_todo.updated_at
        )

        print(f"✓ TodoResponse created: {response}")

        # Serialize to JSON like FastAPI would
        json_data = response.model_dump(mode='json')
        print(f"✓ Serialized to JSON: {json_data}")

        # Verify the id field exists
        assert 'id' in json_data, "id field is missing from serialized response"
        assert json_data['id'] == 1, f"Expected id=1, got {json_data['id']}"

        # Verify datetime fields are properly formatted
        assert 'created_at' in json_data, "created_at field is missing"
        assert 'updated_at' in json_data, "updated_at field is missing"

        print(f"✓ All required fields present: id={json_data['id']}")
        print(f"✓ Datetime format: created_at={json_data['created_at']}")

        return True
    except Exception as e:
        print(f"✗ Error in TodoResponse serialization: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_response_serialization():
    """Test UserPublic/AuthResponse serialization"""
    print("\nTesting UserPublic/AuthResponse serialization...")

    # Create a mock user object
    mock_user = User(
        id="test-user-id",
        email="test@example.com",
        name="Test User",
        hashed_password="hashed_password",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    try:
        # Create UserPublic like the signup endpoint would
        user_public = UserPublic(
            id=mock_user.id,
            email=mock_user.email,
            name=mock_user.name,
            created_at=mock_user.created_at
        )

        print(f"✓ UserPublic created: {user_public}")

        # Create AuthResponse like the signup endpoint would
        auth_response = AuthResponse(
            user=user_public,
            token="fake-jwt-token"
        )

        print(f"✓ AuthResponse created: {auth_response}")

        # Serialize to JSON
        json_data = auth_response.model_dump(mode='json')
        print(f"✓ Serialized to JSON: {json_data}")

        # Verify the user.id field exists
        assert 'user' in json_data, "user field is missing from auth response"
        assert 'id' in json_data['user'], "user.id field is missing"
        assert json_data['user']['id'] == "test-user-id", f"Expected user.id=test-user-id, got {json_data['user']['id']}"

        print(f"✓ All required fields present: user.id={json_data['user']['id']}")

        return True
    except Exception as e:
        print(f"✗ Error in UserPublic/AuthResponse serialization: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing API response serialization...\n")

    todo_success = test_todo_response_serialization()
    user_success = test_user_response_serialization()

    print(f"\nResults:")
    print(f"TodoResponse test: {'PASS' if todo_success else 'FAIL'}")
    print(f"UserPublic test: {'PASS' if user_success else 'FAIL'}")

    if todo_success and user_success:
        print("\n✓ All API response serialization tests PASSED")
        print("The API should now return properly formatted responses that the frontend can handle.")
    else:
        print("\n✗ Some tests FAILED - there may still be issues with API response formatting")