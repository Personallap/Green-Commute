# Authentication Testing Guide

## Quick Start

The authentication endpoints are now live and ready to test!

**Test Credentials:**

- Username: `rahul_student`
- Password: `password123`

(All seeded users have password: `password123`)

## Testing with cURL

### 1. Register a New User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "newuser@example.com", "password": "password123"}'
```

**Expected Response:**

```json
{
  "message": "User registered successfully",
  "user": {...},
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

### 2. Login with Existing User

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "rahul_student", "password": "password123"}'
```

**Expected Response:**

```json
{
  "message": "Login successful",
  "user": {...},
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

### 3. Get Current User (Protected Route)

```bash
# Replace YOUR_ACCESS_TOKEN with the access_token from login
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response:**

```json
{
  "user": {
    "id": 1,
    "username": "rahul_student",
    "email": "rahul@example.com",
    "created_at": "2025-11-22T...",
    "total_co2_saved": 250.5
  }
}
```

### 4. Refresh Access Token

```bash
# Replace YOUR_REFRESH_TOKEN with the refresh_token from login
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

**Expected Response:**

```json
{
  "access_token": "eyJ..."
}
```

## Testing with Postman

1. **Register:**

   - Method: POST
   - URL: `http://localhost:5000/api/auth/register`
   - Body (JSON):
     ```json
     {
       "username": "testuser",
       "email": "test@example.com",
       "password": "password123"
     }
     ```

2. **Login:**

   - Method: POST
   - URL: `http://localhost:5000/api/auth/login`
   - Body (JSON):
     ```json
     {
       "username": "rahul_student",
       "password": "password123"
     }
     ```

3. **Get Profile (Protected):**

   - Method: GET
   - URL: `http://localhost:5000/api/auth/me`
   - Headers:
     - Key: `Authorization`
     - Value: `Bearer <your_access_token>`

4. **Refresh Token:**
   - Method: POST
   - URL: `http://localhost:5000/api/auth/refresh`
   - Headers:
     - Key: `Authorization`
     - Value: `Bearer <your_refresh_token>`

## Error Responses

### Invalid Credentials (401)

```json
{
  "error": "Invalid credentials"
}
```

### User Already Exists (409)

```json
{
  "error": "Username already exists"
}
```

### Missing Token (401)

```json
{
  "msg": "Missing Authorization Header"
}
```

### Expired Token (401)

```json
{
  "msg": "Token has expired"
}
```

## Token Configuration

- **Access Token Expiry:** 1 hour
- **Refresh Token Expiry:** 30 days

## Summary

✅ All authentication endpoints are working!

- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user (requires auth)

The system uses JWT (JSON Web Tokens) for secure, stateless authentication.
