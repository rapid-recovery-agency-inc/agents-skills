from __future__ import annotations

import json
from typing import Any
from contextlib import contextmanager

import httpx

from . import __version__


GITHUB_RAW_BASE = (
    "https://raw.githubusercontent.com/rapid-recovery-agency-inc/agents-skills/refs/heads/main/cli"
)

DEFAULT_TIMEOUT = httpx.Timeout(10.0, read=30.0)


@contextmanager
def get_http_client(timeout: httpx.Timeout | None = None) -> httpx.Client:
    """Create an HTTP client with proper session management.

    Uses context manager for automatic cleanup and includes
    proper User-Agent header with version information.
    """
    client = httpx.Client(
        headers={"User-Agent": f"agents-skills/{__version__}"},
        timeout=timeout or DEFAULT_TIMEOUT,
        follow_redirects=True,
    )
    try:
        yield client
    finally:
        client.close()


def fetch_json(url: str, timeout: httpx.Timeout | None = None) -> dict[str, Any]:
    """Fetch and parse JSON from a URL.

    Args:
        url: The URL to fetch JSON from
        timeout: Optional custom timeout

    Returns:
        Parsed JSON response as a dictionary

    Raises:
        httpx.HTTPStatusError: On HTTP errors
        httpx.ConnectError: On connection failures
        httpx.TimeoutException: On timeout

    """
    with get_http_client(timeout) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def fetch_registry() -> dict[str, Any]:
    """Fetch the registry.json from GitHub.

    Returns:
        The parsed registry data

    Raises:
        CliError: On any fetch failure

    """
    from .core import CliError  # noqa: PLC0415

    try:
        return fetch_json(f"{GITHUB_RAW_BASE}/registry.json")
    except httpx.HTTPStatusError as exc:
        raise CliError(f"Failed to fetch registry (HTTP {exc.response.status_code})") from exc
    except httpx.ConnectError as exc:
        raise CliError("Cannot connect to GitHub (check network)") from exc
    except httpx.TimeoutException as exc:
        raise CliError("Request timed out") from exc
    except json.JSONDecodeError as exc:
        raise CliError(f"Invalid JSON in registry: {exc}") from exc


def fetch_schema() -> dict[str, Any]:
    """Fetch the registry.schema.json from GitHub."""
    from .core import CliError  # noqa: PLC0415

    try:
        return fetch_json(f"{GITHUB_RAW_BASE}/registry.schema.json")
    except httpx.HTTPStatusError as exc:
        raise CliError(f"Failed to fetch schema (HTTP {exc.response.status_code})") from exc
    except httpx.ConnectError as exc:
        raise CliError("Cannot connect to GitHub (check network)") from exc
    except httpx.TimeoutException as exc:
        raise CliError("Request timed out") from exc
    except json.JSONDecodeError as exc:
        raise CliError(f"Invalid JSON in schema: {exc}") from exc


def fetch_tags_vocab() -> list[str]:
    """Fetch the tags.vocab.json from GitHub."""
    from .core import CliError  # noqa: PLC0415

    try:
        return fetch_json(f"{GITHUB_RAW_BASE}/tags.vocab.json")
    except httpx.HTTPStatusError as exc:
        raise CliError(f"Failed to fetch tags vocab (HTTP {exc.response.status_code})") from exc
    except httpx.ConnectError as exc:
        raise CliError("Cannot connect to GitHub (check network)") from exc
    except httpx.TimeoutException as exc:
        raise CliError("Request timed out") from exc
    except json.JSONDecodeError as exc:
        raise CliError(f"Invalid JSON in tags vocab: {exc}") from exc


def fetch_version() -> str | None:
    """Fetch the version.json from GitHub.

    Returns:
        The version string, or None if not available

    """
    try:
        data = fetch_json(f"{GITHUB_RAW_BASE}/version.json")
        return data.get("version")
    except Exception:
        return None
