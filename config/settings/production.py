from urllib.parse import urlsplit

from config.env import env, env_bool, env_list, env_required
from config.settings.base import *  # noqa: F403

DEBUG = False

SECRET_KEY = env_required("SECRET_KEY")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")

if not ALLOWED_HOSTS:
    raise RuntimeError(
        "ALLOWED_HOSTS must contain at least one host in production."
    )

APP_URL = env_required("APP_URL").rstrip("/")
app_url_parts = urlsplit(APP_URL)
if app_url_parts.scheme != "https" or not app_url_parts.netloc:
    raise RuntimeError("APP_URL must be an absolute HTTPS URL in production.")

SECURE_SSL_REDIRECT = env_bool(
    "SECURE_SSL_REDIRECT",
    True,
)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
# Preload is an irreversible domain-wide operational commitment and is not
# enabled automatically. HSTS itself remains enabled for one year.
SILENCED_SYSTEM_CHECKS = ["security.W021"]

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
)

if not CSRF_TRUSTED_ORIGINS:
    raise RuntimeError(
        "CSRF_TRUSTED_ORIGINS must contain the public HTTPS origin in production."
    )

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# SMTP is provider-neutral: Railway can supply credentials for any SMTP service.
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = env("EMAIL_HOST", "")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_USERNAME", "")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_TIMEOUT = int(env("EMAIL_TIMEOUT", "10"))


# Production static asset serving.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
