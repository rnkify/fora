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

Browser tests start an isolated local Django server and exercise Chromium at
desktop, tablet, and mobile widths:

```shell
npm run test:browser
```

## Production

The Docker image collects static assets and starts Gunicorn with Django's ASGI
application. The startup script applies pending migrations before serving traffic.
Railway must provide `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, `APP_URL`, and
the relevant email settings from `.env.example`. Set `CSRF_TRUSTED_ORIGINS` to the
public HTTPS origin and `INQUIRY_NOTIFICATION_EMAIL` to the internal recipient.
Production startup rejects a missing or non-PostgreSQL `DATABASE_URL`; it never
falls back to SQLite or a local development database.

Email is provider-neutral SMTP. When inquiry notifications are enabled, configure
`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USERNAME`, `EMAIL_PASSWORD`, `EMAIL_USE_TLS`,
`DEFAULT_FROM_EMAIL`, and `INQUIRY_NOTIFICATION_EMAIL`. Notification delivery
failures are logged and do not roll back a persisted inquiry.

`/health/` is the process liveness endpoint. `/ready/` verifies the database
connection and should be used where a readiness check is supported.

Before release, run:

```shell
npm run css:build
python -m ruff check apps config content tests
python manage.py check
python -m pytest tests -q
python manage.py makemigrations --check --dry-run
DJANGO_SETTINGS_MODULE=config.settings.production python manage.py check --deploy
docker build -t fora .
```

Apply migrations before serving traffic; the included startup script does this.
Create the first operator with `python manage.py createsuperuser`. Configure the
platform health check to `/health/` and use `/ready/` where database-aware probes
are supported.

PostgreSQL backups remain an operational responsibility. Enable automated,
encrypted provider backups, define retention appropriate to the business, keep at
least one copy outside the primary database lifecycle, and test restoration before
launch and periodically thereafter. Never treat an untested backup as recoverable.
