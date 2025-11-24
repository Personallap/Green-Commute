"""
Reset script to clear all trip history and CO2 savings for a user
Usage: python reset_user_data.py
"""

from app import create_app, db
from app.models import User, Trip

def reset_all_trips():
    """Reset all trips and CO2 savings for all users"""
    app = create_app()
    
    with app.app_context():
        try:
            # Delete all trips
            deleted_trips = Trip.query.delete()
            print(f"Deleted {deleted_trips} trips")
            
            # Reset CO2 savings for all users
            users = User.query.all()
            for user in users:
                user.total_co2_saved = 0
                print(f"Reset CO2 savings for user: {user.username}")
            
            db.session.commit()
            print("\n✓ Successfully reset all trip data and CO2 savings!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

def reset_user_trips(user_id):
    """Reset trips and CO2 savings for a specific user"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get the user
            user = User.query.get(user_id)
            if not user:
                print(f"User with ID {user_id} not found")
                return
            
            # Delete user's trips
            deleted_trips = Trip.query.filter_by(user_id=user_id).delete()
            print(f"Deleted {deleted_trips} trips for user: {user.username}")
            
            # Reset CO2 savings
            user.total_co2_saved = 0
            
            db.session.commit()
            print(f"\n✓ Successfully reset data for user: {user.username}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

if __name__ == '__main__':
    print("=" * 50)
    print("GreenCommute - Reset User Data")
    print("=" * 50)
    
    choice = input("\n1. Reset ALL users' data\n2. Reset specific user's data\n\nEnter choice (1 or 2): ")
    
    if choice == '1':
        confirm = input("\nThis will delete ALL trip data for ALL users. Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            reset_all_trips()
        else:
            print("Cancelled.")
    elif choice == '2':
        user_id = input("Enter user ID: ")
        try:
            reset_user_trips(int(user_id))
        except ValueError:
            print("Invalid user ID")
    else:
        print("Invalid choice")
