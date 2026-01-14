#!/usr/bin/env python3
"""
Quick test script to verify the API endpoints without restarting server
"""
import sys
import os
sys.path.insert(0, '/mnt/c/Users/NBK COMPUTER/Desktop/hackathon2/phase2part2')

# Import and test the datetime serialization directly
from datetime import datetime
from models import Todo
from schemas import TodoResponse

def test_serialization():
    """Test if datetime serialization works correctly"""
    print("Testing datetime serialization...")

    # Create a mock todo object similar to what comes from the database
    mock_todo = Todo(
        id=1,
        user_id="test-user-id",
        title="Test Todo",
        description="Test Description",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Try to create a TodoResponse from it
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

        print(f"✓ TodoResponse created successfully: {response}")
        print(f"✓ Created at type: {type(response.created_at)}, value: {response.created_at}")
        print(f"✓ Updated at type: {type(response.updated_at)}, value: {response.updated_at}")

        # Test conversion to dict (simulating JSON serialization)
        response_dict = response.model_dump()
        print(f"✓ Model dump successful: {response_dict['id']}, dates: {response_dict['created_at']}, {response_dict['updated_at']}")

        return True
    except Exception as e:
        print(f"✗ Error creating TodoResponse: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_serialization()
    if success:
        print("\n✓ Datetime serialization test PASSED")
    else:
        print("\n✗ Datetime serialization test FAILED")