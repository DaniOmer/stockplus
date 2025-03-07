# User Module

This module handles user authentication, registration, verification, and integration with Stripe for subscription management.

## Features

- User registration with email or phone number
- Account verification via email link or SMS code
- Password reset functionality
- JWT-based authentication
- Stripe customer creation for verified users
- Clean architecture with domain-driven design

## Architecture

The user module follows a clean architecture approach with the following layers:

### Domain Layer

- **Entities**: Core business objects (User, Invitation)
- **Exceptions**: Domain-specific exceptions

### Application Layer

- **Interfaces**: Repository interfaces
- **Services**: Business logic and use cases

### Infrastructure Layer

- **Models**: Django ORM models
- **Repositories**: Data access implementations
- **Signals**: Event handlers
- **Utils**: Helper functions

### Interface Layer

- **Serializers**: Data validation and transformation
- **Views**: API endpoints
- **URLs**: Routing configuration

## Authentication Flow

1. **Registration**:

   - User registers with email/phone and password
   - Verification token is generated
   - Verification email/SMS is sent

2. **Verification**:

   - User clicks verification link or enters code
   - Account is marked as verified
   - Stripe customer is created

3. **Login**:
   - User provides credentials
   - JWT tokens are issued
   - Access token is used for API requests

## Password Reset Flow

1. **Request Reset**:

   - User requests password reset with email/phone
   - Reset token is generated
   - Reset email/SMS is sent

2. **Verify Token**:

   - User enters reset token
   - Token is verified

3. **Reset Password**:
   - User enters new password
   - Password is updated

## Stripe Integration

- Stripe customer is created when a user is verified
- Customer is linked to subscription plans
- Payments are processed through Stripe

## API Endpoints

### Authentication

- `POST /api/auth/register/`: Register a new user
- `POST /api/auth/login/`: Login and get JWT tokens
- `POST /api/auth/token/`: Get JWT tokens
- `POST /api/auth/token/refresh/`: Refresh JWT token
- `POST /api/auth/token/verify/`: Verify JWT token

### Email Verification

- `POST /api/auth/email-verify/`: Verify email with token
- `POST /api/auth/email-verify/resend/`: Resend verification email

### Password Reset

- `POST /api/auth/password-reset/`: Request password reset
- `POST /api/auth/password-reset/verify/`: Verify password reset token
- `POST /api/auth/password-reset/confirm/`: Confirm password reset

## Usage Examples

### Registration

```python
import requests

response = requests.post(
    'http://localhost:8000/api/auth/register/',
    json={
        'email': 'user@example.com',
        'password': 'securepassword',
        'first_name': 'John',
        'last_name': 'Doe'
    }
)
print(response.json())
```

### Login

```python
import requests

response = requests.post(
    'http://localhost:8000/api/auth/login/',
    json={
        'email': 'user@example.com',
        'password': 'securepassword'
    }
)
tokens = response.json()['tokens']
access_token = tokens['access']
refresh_token = tokens['refresh']
print(f"Access Token: {access_token}")
```

### Verify Email

```python
import requests

response = requests.post(
    'http://localhost:8000/api/auth/email-verify/',
    json={
        'token': '123456'  # Token received in email
    }
)
print(response.json())
```

### Reset Password

```python
# Request reset
response = requests.post(
    'http://localhost:8000/api/auth/password-reset/',
    json={
        'email': 'user@example.com'
    }
)

# Verify token
response = requests.post(
    'http://localhost:8000/api/auth/password-reset/verify/',
    json={
        'token': '123456'  # Token received in email
    }
)

# Confirm reset
response = requests.post(
    'http://localhost:8000/api/auth/password-reset/confirm/',
    json={
        'token': '123456',
        'new_password': 'newsecurepassword',
        'confirm_password': 'newsecurepassword'
    }
)
```
