"""
Interactive Authentication Test CLI
Allows you to login with username/password and view user profile.
"""

import requests
import json
from getpass import getpass

BASE_URL = "http://localhost:5000/api"

def display_user_profile(user_data):
    """Display user profile in a formatted way."""
    print("\n" + "=" * 80)
    print("📋 USER PROFILE")
    print("=" * 80)
    print(f"👤 Username: {user_data.get('username')}")
    print(f"📧 Email: {user_data.get('email')}")
    print(f"🆔 User ID: {user_data.get('id')}")
    print(f"🌱 Total CO2 Saved: {user_data.get('total_co2_saved')}g")
    print(f"📅 Account Created: {user_data.get('created_at')}")
    print("=" * 80)


def search_user_in_db(username):
    """Search for a user in the database by username."""
    from app import create_app, db
    from app.models import User
    
    app = create_app()
    with app.app_context():
        # Search for user by username (case-insensitive)
        user = User.query.filter(User.username.ilike(f'%{username}%')).all()
        
        if not user:
            print(f"\n❌ No users found matching '{username}'")
            return
        
        print(f"\n🔍 Found {len(user)} user(s) matching '{username}':")
        print("-" * 80)
        for u in user:
            print(f"  • {u.username} ({u.email}) - CO2 Saved: {u.total_co2_saved}g")
        print("-" * 80)


def interactive_login():
    """Interactive login flow."""
    print("=" * 80)
    print("🔐 GreenCommute Authentication Test")
    print("=" * 80)
    
    # Get credentials from user
    print("\n📝 Please enter your credentials:")
    username = input("Username: ").strip()
    password = getpass("Password: ")  # Hidden input for password
    
    if not username or not password:
        print("\n❌ Username and password are required!")
        return
    
    # Attempt login
    print("\n🔄 Attempting to login...")
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            print("✅ Login successful!\n")
            data = response.json()
            
            # Display user profile from login response
            display_user_profile(data['user'])
            
            # Store token for authenticated requests
            access_token = data['access_token']
            
            # Make authenticated request to get fresh profile
            print("\n🔄 Fetching latest profile from server...")
            headers = {"Authorization": f"Bearer {access_token}"}
            me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            
            if me_response.status_code == 200:
                print("✅ Profile fetched successfully!")
                display_user_profile(me_response.json()['user'])
            
            # Search for user in database
            print(f"\n🔍 Searching database for users matching '{username}'...")
            search_user_in_db(username)
            
            # Show token info
            print("\n🔑 Access Token (valid for 1 hour):")
            print(f"   {access_token[:50]}...")
            
        elif response.status_code == 401:
            print(f"\n❌ Login failed: Invalid credentials")
            print("💡 Hint: Try these test credentials:")
            print("   Username: rahul_student")
            print("   Password: password123")
        else:
            print(f"\n❌ Login failed: {response.json().get('error', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("Make sure the Flask server is running on http://localhost:5000")
        print("Run: python run.py")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")


def list_available_users():
    """List all available test users in the database."""
    from app import create_app, db
    from app.models import User
    
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        print("\n" + "=" * 80)
        print("📋 AVAILABLE TEST USERS (all have password: 'password123')")
        print("=" * 80)
        for user in users:
            print(f"  • Username: {user.username:20} | Email: {user.email}")
        print("=" * 80)


if __name__ == '__main__':
    print("\n🌱 Welcome to GreenCommute Interactive Auth Test!\n")
    
    # Show available users
    print("Loading available users from database...")
    try:
        list_available_users()
    except Exception as e:
        print(f"⚠️ Could not load users from database: {e}")
    
    # Start interactive login
    while True:
        interactive_login()
        
        print("\n" + "=" * 80)
        again = input("\n🔄 Try another login? (yes/no): ").strip().lower()
        if again not in ['yes', 'y']:
            print("\n👋 Thank you for using GreenCommute!")
            break
