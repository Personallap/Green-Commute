"""
Quick test to verify registration saves to database.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

print("=" * 80)
print("Testing User Registration and Database Storage")
print("=" * 80)

# Create a unique username
timestamp = datetime.now().strftime("%H%M%S")
test_data = {
    "username": f"dbtest_{timestamp}",
    "email": f"dbtest_{timestamp}@test.com",
    "password": "testpass123"
}

print(f"\n1. Registering new user: {test_data['username']}")
print(f"   Email: {test_data['email']}")

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=test_data)
    print(f"\n2. Response Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print("✅ Registration successful!")
        print(f"   User ID: {data['user']['id']}")
        print(f"   Username: {data['user']['username']}")
        print(f"   Email: {data['user']['email']}")
        
        # Now verify it's in the database
        print("\n3. Verifying user exists in database...")
        from app import create_app, db
        from app.models import User
        
        app = create_app()
        with app.app_context():
            user = User.query.filter_by(username=test_data['username']).first()
            if user:
                print(f"✅ User found in database!")
                print(f"   ID: {user.id}")
                print(f"   Username: {user.username}")
                print(f"   Email: {user.email}")
                print(f"   Has password hash: {bool(user.password_hash)}")
                print(f"   Password hash length: {len(user.password_hash) if user.password_hash else 0}")
                
                # Test password verification
                print("\n4. Testing password verification...")
                if user.check_password("testpass123"):
                    print("✅ Password verification works!")
                else:
                    print("❌ Password verification failed!")
            else:
                print("❌ User NOT found in database!")
    else:
        print(f"❌ Registration failed: {response.json()}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("Test Complete")
print("=" * 80)
