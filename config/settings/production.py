from config.env import env_bool, env_list, env_required
from config.settings.base import *  # noqa: F403

DEBUG = False

SECRET_KEY = env_required("SECRET_KEY")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")

if not ALLOWED_HOSTS:
    raise RuntimeError(
        "ALLOWED_HOSTS must contain at least one host in production."
    )

SECURE_SSL_REDIRECT = env_bool(
    "SECURE_SSL_REDIRECT",
    True,
)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
)
