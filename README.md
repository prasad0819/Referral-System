# Referral System API

This is a **Referral System API** built with **Django Rest Framework (DRF)**. The system includes functionality for managing referrals. It uses **JWT** for authentication.

---

## Requirements

- Python 3.12+
- Django 5.1+
- Django Rest Framework 3.15+
- Simple JWT 5.3+
- Short UUID 1.0+

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/prasad0819/Referral-System.git
cd referral_system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

---

## API Endpoints

### Authentication

* POST `/api/token` : Obtain access and refresh tokens.

    - Request

        ```json
        {
        "email": "user@example.com",
        "password": "password123"
        }
        ```
    
    - Response

        ```json
        {
            "refresh": "eyJhbGciOiJIUzI1NiIs...",
            "access": "eyJhbGciOiJIUzI1NiIs...",
            "id": 1,
            "email": "user@example.com",
        }
        ```

* POST `/api/token/refresh/` : Refresh the access token.


### Referral System

* POST `/api/user-profiles/` : Create new User Profile

    - Request

        ```json
        {
            "user": {
                "email": "user@example.com",
                "password": "password123"
            },
            "full_name": "John Doe",
            "phone": "+14378929192",
            "city": "Mumbai",
            "referrer_code": ""
        }
        ```
        Referrer Code is optional, or it can be a valid 8 character referral code.
    
    - Response

        ```json
        {
            "id": 10,
            "user": {
                "email": "user@example.com"
            },
            "full_name": "John Doe",
            "phone": "+14378929192",
            "city": "Mumbai",
            "referral_code": "sG7a5uNb5k",
            "created_at": "2024-11-25T19:19:14.135870Z",
            "referred_by": null
        }
        ```
        Note that the referral code for this user was auto-generated.
<br>

* GET `/api/user-profiles/{id}` : Get User Profile details


    - Request : Make sure to add the Authorization header using access token

        `Authorization: Bearer eyJhbGciOiJIUzI1NiIsIn...`
    
    - Response

        ```json
        {
            "id": 6,
            "user": {
                "email": "john@example.com"
            },
            "full_name": "John Doe",
            "phone": "+14378929192",
            "city": "Mumbai",
            "referral_code": "sG7a5uNb5k",
            "created_at": "2024-11-25T15:40:44.898842Z",
            "referred_by": null
        }
        ```
<br>

* GET `/api/user-profiles/{id}/referees` : Get Referees for a user i.e. users that were referred by this user

    - Request : Make sure to add the Authorization header using access token

        `Authorization: Bearer eyJhbGciOiJIUzI1NiIsIn...`

    
    - Response

        ```json
        [
            {
                "full_name":"Jane Doe",
                "email":"jane@example.com",
                "created_at":"2024-11-25T15:49:01.502165Z"
            },
            {
                "full_name":"John Smith",
                "email":"smith@example.com",
                "created_at":"2024-11-25T19:49:01.502165Z"
            },
        ]
        ```

