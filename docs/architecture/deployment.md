# Fora Deployment Architecture

## V1 topology

Fora V1 uses a single deployable Django application with PostgreSQL.

Production topology:

Git repository
→ container build
→ Django ASGI application
→ PostgreSQL

## Application server

Production entrypoint:

- Gunicorn
- Uvicorn worker
- Django ASGI application

## Environment

Production configuration is supplied through environment variables.

Secrets must never be committed.

Required production values include:

- SECRET_KEY
- DATABASE_URL
- ALLOWED_HOSTS
- APP_URL

Additional integration credentials are added only when the associated
feature is enabled.

## Database

Production uses PostgreSQL.

The production application role must not receive:

- SUPERUSER
- CREATEDB
- CREATEROLE

Database schema changes are performed using Django migrations.

## Static assets

Django collectstatic builds the production static asset directory.

The storage architecture can later move behind CDN or object storage
without changing application business logic.

## HTTPS

Production must operate behind HTTPS.

Production Django settings enable:

- secure cookies
- SSL redirect
- HSTS
- strict referrer policy

## Portability

Fora is containerized so the deployment platform can be changed without
rewriting the application.

Railway is the intended initial host, but the application remains a
standard Django/PostgreSQL deployment.
