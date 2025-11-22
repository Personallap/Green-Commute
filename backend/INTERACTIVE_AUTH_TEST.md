# Interactive Authentication Test - README

## Overview

`test_interactive_auth.py` is an interactive CLI tool to test the authentication system by logging in with real credentials and viewing user profiles.

## Features

- 📝 **Interactive Login:** Prompts for username and password
- 🔒 **Secure Password Input:** Password is hidden while typing
- 👤 **Profile Display:** Shows complete user profile after login
- 🔍 **Database Search:** Searches for users matching the entered username
- 🔑 **Token Display:** Shows the generated JWT access token
- 📋 **User List:** Displays all available test users from the database

## Usage

### Run the Interactive Test

```bash
cd backend
py test_interactive_auth.py
```

### Example Session

```
🌱 Welcome to GreenCommute Interactive Auth Test!

Loading available users from database...

================================================================================
📋 AVAILABLE TEST USERS (all have password: 'password123')
================================================================================
  • Username: rahul_student        | Email: rahul@example.com
  • Username: shreya_tech          | Email: shreya@example.com
  • Username: karan_eco            | Email: karan@example.com
  • Username: priya_commuter       | Email: priya@example.com
  • Username: amit_green           | Email: amit@example.com
================================================================================

================================================================================
🔐 GreenCommute Authentication Test
================================================================================

📝 Please enter your credentials:
Username: rahul_student
Password: *********** (hidden)

🔄 Attempting to login...
✅ Login successful!

================================================================================
📋 USER PROFILE
================================================================================
👤 Username: rahul_student
📧 Email: rahul@example.com
🆔 User ID: 1
🌱 Total CO2 Saved: 250.5g
📅 Account Created: 2025-11-22T10:28:35.081019
================================================================================

🔄 Fetching latest profile from server...
✅ Profile fetched successfully!

🔍 Searching database for users matching 'rahul_student'...

🔍 Found 1 user(s) matching 'rahul_student':
--------------------------------------------------------------------------------
  • rahul_student (rahul@example.com) - CO2 Saved: 250.5g
--------------------------------------------------------------------------------

🔑 Access Token (valid for 1 hour):
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI...

================================================================================

🔄 Try another login? (yes/no): no

👋 Thank you for using GreenCommute!
```

## What It Does

1. **Loads Available Users:** Shows all users in the database for reference
2. **Accepts Credentials:** Prompts for username (visible) and password (hidden)
3. **Performs Login:** Sends credentials to `/api/auth/login`
4. **Displays Profile:** Shows user details from the login response
5. **Fetches Latest Data:** Makes authenticated request to `/api/auth/me`
6. **Searches Database:** Queries the database directly for matching usernames
7. **Shows Token:** Displays the JWT access token

## Test Credentials

All seeded users have the password: `password123`

Available usernames:

- `rahul_student`
- `shreya_tech`
- `karan_eco`
- `priya_commuter`
- `amit_green`

## Requirements

- Flask server must be running (`py run.py`)
- `requests` library must be installed (`py -m pip install requests`)

## Error Handling

### Invalid Credentials

```
❌ Login failed: Invalid credentials
💡 Hint: Try these test credentials:
   Username: rahul_student
   Password: password123
```

### Server Not Running

```
❌ Error: Could not connect to the server.
Make sure the Flask server is running on http://localhost:5000
Run: python run.py
```

## Features Demonstrated

✅ **Login Flow:** Complete authentication process
✅ **Profile Retrieval:** Protected endpoint access with JWT
✅ **Database Queries:** Direct database search functionality
✅ **Token Management:** JWT token generation and usage
✅ **Error Handling:** Graceful handling of invalid credentials
✅ **Security:** Password masking with `getpass`
