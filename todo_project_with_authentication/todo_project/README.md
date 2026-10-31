# Django + Postgres Todo App

A small multi-user todo app built with Django 5.x and PostgreSQL (psycopg 3). Users must sign in or create an account before accessing Todo. Each Todo is private to its owner.

Features:
- Sign in and sign up from the home page (`/`).
- Add, edit, complete, delete, and filter todos (all/active/done).
- Clear completed todos for the signed-in user only.
- User-specific todo access enforced on the server.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # edit values if you like
docker compose up -d db       # starts Postgres 16 on localhost:5432

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Open http://127.0.0.1:8000/. The home page displays both the sign-in and registration forms. After authentication, the user is redirected to `/todos/`.

## Tests

```bash
python manage.py test
```

The test runner creates and drops its own `test_<DB_NAME>` database, so the DB user needs `CREATEDB`. The Docker image's `POSTGRES_USER` is a superuser, so this works out of the box.

## Authentication and data ownership

Django's built-in authentication system handles passwords and sessions. The home page is the sign-in page; registration is also available there. All Todo views require an authenticated user, and every query or object lookup is scoped to `request.user`.

The `owner` field is nullable in the migration only to preserve compatibility with Todo rows created before authentication was added. Such legacy rows have no owner and are intentionally not shown to any account. New todos always receive their owner from the authenticated request. If an existing database contains old todos that must be retained, assign each row to the appropriate user before considering a later migration that makes `owner` non-nullable.

## Layout

- `config/` – settings (all DB and secret values come from `.env`), root URLs, WSGI
- `todos/` – model, form, views, URLs, admin, templates, tests

## Before deploying

Set a real `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, and a proper `DJANGO_ALLOWED_HOSTS`, and serve static files via a production setup.
