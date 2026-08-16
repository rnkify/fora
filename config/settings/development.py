from config.env import env_bool, env_list
from config.settings.base import *  # noqa: F403

DEBUG = env_bool("DEBUG", True)

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    ["127.0.0.1", "localhost"],
)

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)
