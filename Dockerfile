FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./

COPY apps ./apps
COPY config ./config
COPY content ./content
COPY manage.py ./

RUN python -m pip install --upgrade pip \
    && python -m pip install .

COPY templates ./templates
COPY static ./static
COPY design ./design

RUN SECRET_KEY=build-only-secret \
    ALLOWED_HOSTS=localhost \
    DATABASE_URL=postgresql://placeholder:placeholder@localhost:5432/placeholder \
    python manage.py collectstatic \
    --noinput \
    --settings=config.settings.production

EXPOSE 8000

CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-"]
