# Fora

Fora is a configurable AI systems and growth studio platform.

## V1 purpose

Fora V1 is designed to:

- present and sell professional services
- capture and qualify leads
- manage clients and projects
- support repeatable service delivery
- provide lightweight internal operations tooling
- remain ready for future billing and product expansion

## Architecture

Fora uses a modular Django monolith.

Core principles:

1. Stable application logic is separated from frequently changing business configuration.
2. Branding, services, pricing, navigation, marketing content, feature flags, and design values are centralized.
3. Stable internal IDs are separate from editable public labels.
4. Secrets and environment-specific credentials are never committed.
5. External providers are accessed through replaceable interfaces.
6. V1 stays within the approved feature boundary.

## Development stack

- Python 3.14
- Django 5.2 LTS
- PostgreSQL
- Psycopg 3
- Django templates
- HTMX where justified
- Tailwind CSS 4
- Gunicorn + Uvicorn for production
- Docker-compatible deployment

## Local development

Create and activate a Python 3.14 virtual environment, install the project with
development dependencies, copy `.env.example` to `.env`, and configure a local
PostgreSQL database. Then run:

```shell
python manage.py migrate
npm install
npm run css:build
python manage.py runserver
```

The test suite uses an isolated SQLite database and does not connect to the
development or production database:

```shell
pytest
```

## Production

The Docker image collects static assets and starts Gunicorn with Django's ASGI
application. The startup script applies pending migrations before serving traffic.
Railway must provide `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, `APP_URL`, and
the relevant email settings from `.env.example`. Set `CSRF_TRUSTED_ORIGINS` to the
public HTTPS origin and `INQUIRY_NOTIFICATION_EMAIL` to the internal recipient.

`/health/` is the process liveness endpoint. `/ready/` verifies the database
connection and should be used where a readiness check is supported.
