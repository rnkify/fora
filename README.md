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

The complete development instructions will be added as the foundation is implemented.
