from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def env_required(name: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        raise RuntimeError(f"Required environment variable {name!r} is missing.")

    return value.strip()


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    normalized = value.strip().lower()

    if normalized in {"1", "true", "yes", "on"}:
        return True

    if normalized in {"0", "false", "no", "off"}:
        return False

    raise RuntimeError(
        f"Environment variable {name!r} must be a boolean value."
    )


def env_list(
    name: str,
    default: list[str] | None = None,
) -> list[str]:
    value = os.getenv(name)

    if value is None:
        return list(default or [])

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]
