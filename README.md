# 24b0644-django-unchained
# 🤠 Bounty Board API — wildwest

A Django REST Framework project where users can post, track, and manage "wanted" bounties, Wild West style. Built with JWT authentication, per-user caching, and rate limiting.

## Project Overview

Bounty Board lets registered users post bounties on targets, complete with a reward amount, status (`wanted` / `captured`), description, and location. Every user manages their own bounties — nobody can read, edit, or delete another user's listings.

## Features

- JWT-based authentication (register, login, refresh)
- Full CRUD on bounties, scoped to the authenticated owner
- Owner-only permissions on retrieve/update/delete
- Response caching on the bounty list endpoint (60s), auto-invalidated on write
- Anonymous and authenticated rate limiting
- Clean serializer-level validation
- Django admin integration with search and filters

## Technologies Used

- Python 3 / Django 5+
- Django REST Framework
- djangorestframework-simplejwt
- django-cors-headers
- SQLite

## Installation

```bash
git clone <your-repo-url>
cd wildwest
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Folder Structure

```
wildwest/
├── manage.py
├── requirements.txt
├── README.md
├── wildwest/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── bounties/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── permissions.py
    ├── serializers.py
    ├── signals.py
    ├── throttles.py
    ├── urls.py
    ├── views.py
    └── migrations/
```

## API Endpoints

| Method | Endpoint                  | Description             | Auth Required |
|--------|----------------------------|--------------------------|---------------|
| POST   | `/api/auth/register/`      | Register a new user      | No            |
| POST   | `/api/auth/login/`         | Obtain JWT token pair    | No            |
| POST   | `/api/auth/refresh/`       | Refresh access token     | No            |
| GET    | `/api/bounties/`           | List your bounties       | Yes           |
| POST   | `/api/bounties/`           | Create a bounty          | Yes           |
| GET    | `/api/bounties/<id>/`      | Retrieve a bounty        | Yes (owner)   |
| PUT    | `/api/bounties/<id>/`      | Full update a bounty     | Yes (owner)   |
| PATCH  | `/api/bounties/<id>/`      | Partial update a bounty  | Yes (owner)   |
| DELETE | `/api/bounties/<id>/`      | Delete a bounty          | Yes (owner)   |

## Authentication

This API uses **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`. Include the access token on every protected request:

```
Authorization: Bearer <access_token>
```

## JWT Usage

1. Register a user via `/api/auth/register/`.
2. Log in via `/api/auth/login/` to receive an `access` and `refresh` token.
3. Use the `access` token in the `Authorization` header for all bounty endpoints.
4. When the access token expires, call `/api/auth/refresh/` with the `refresh` token to get a new access token.

## Bonus Features

### Rate Limiting

- Anonymous users: **20 requests/hour**
- Authenticated users: **100 requests/hour**

Implemented with DRF's `AnonRateThrottle` / `UserRateThrottle` in `bounties/throttles.py` and wired globally in `settings.py`.

### Caching

- The bounty list endpoint (`GET /api/bounties/`) is cached per-user for **60 seconds** using Django's local memory cache.
- The cache is automatically invalidated via `post_save` / `post_delete` signals whenever a bounty is created, updated, or deleted.

## Example Requests

**Register**
```json
POST /api/auth/register/
{
  "username": "sheriff_jane",
  "password": "strongpassword123"
}
```

**Login**
```json
POST /api/auth/login/
{
  "username": "sheriff_jane",
  "password": "strongpassword123"
}
```

**Create Bounty**
```json
POST /api/bounties/
Authorization: Bearer <access_token>
{
  "target_name": "Billy the Kid",
  "reward": "500.00",
  "status": "wanted",
  "description": "Last seen near the old saloon.",
  "location": "Tombstone, AZ"
}
```

## Example Responses

**Login Response**
```json
{
  "refresh": "eyJhbGciOi...",
  "access": "eyJhbGciOi..."
}
```

**Bounty List Response**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "target_name": "Billy the Kid",
      "reward": "500.00",
      "status": "wanted",
      "description": "Last seen near the old saloon.",
      "location": "Tombstone, AZ",
      "created_at": "2026-07-03T10:00:00Z",
      "owner": "sheriff_jane"
    }
  ]
}
```

## Running Locally

```bash
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` for the Django admin, or `http://127.0.0.1:8000/api/` for the API root.

## Future Improvements

- Add refresh token rotation and blacklisting
- Add bounty image uploads
- Add public/shared bounty boards with pagination filters
- Add search and ordering endpoints (by reward, date, status)
- Switch to PostgreSQL for production
- Add automated test suite (pytest + DRF test client)