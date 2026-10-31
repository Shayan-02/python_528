# Django + Postgres Todo App

A small todo app: add, edit, complete, delete, filter (all/active/done), and clear completed. Django 5.x with PostgreSQL via psycopg 3.

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

Open http://127.0.0.1:8000/.

## Tests

```bash
python manage.py test
```

The test runner creates and drops its own `test_<DB_NAME>` database, so the DB user needs `CREATEDB`. The Docker image's `POSTGRES_USER` is a superuser, so this works out of the box.

## Layout

- `config/` – settings (all DB and secret values come from `.env`), root URLs, WSGI
- `todos/` – model, form, views, URLs, admin, templates, tests

## Before deploying

Set a real `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, and a proper `DJANGO_ALLOWED_HOSTS`, and serve static files via a production setup.
