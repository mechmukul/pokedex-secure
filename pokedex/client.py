"""Secure client for the public PokeAPI.

Security controls demonstrated here:
- Strict input validation (allow-list regex) before a value ever reaches a URL.
- Fixed, hard-coded API host so user input cannot redirect the request (SSRF-safe).
- Enforced request timeouts and TLS verification (never disabled).
- No secrets in code; nothing sensitive logged.
- Defensive parsing: we only read the fields we expect.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import quote

import requests

API_BASE = "https://pokeapi.co/api/v2"
REQUEST_TIMEOUT = 10  # seconds; bandit B113 guard
# Pokemon names are lowercase letters, digits, and hyphens (e.g. "mr-mime"). Ids are digits.
_VALID_QUERY = re.compile(r"^[a-z0-9-]{1,50}$")


class InvalidQuery(ValueError):
    """Raised when a caller-supplied name or id fails validation."""


class PokemonNotFound(LookupError):
    """Raised when the PokeAPI has no such Pokemon."""


@dataclass(frozen=True)
class Pokemon:
    id: int
    name: str
    height: int
    weight: int
    types: tuple[str, ...]
    base_stats: dict[str, int]


def normalise_query(raw: str) -> str:
    """Validate and normalise a user-supplied name or id. Never trust the caller."""
    if not isinstance(raw, str):
        raise InvalidQuery("query must be a string")
    q = raw.strip().lower()
    if not _VALID_QUERY.match(q):
        raise InvalidQuery(
            "query must be 1-50 chars of lowercase letters, digits, or hyphens"
        )
    return q


def get_pokemon(raw_query: str, *, session: requests.Session | None = None) -> Pokemon:
    """Fetch a Pokemon by name or id from the PokeAPI, safely."""
    query = normalise_query(raw_query)
    # quote() is belt-and-braces; validation already guarantees a safe value.
    url = f"{API_BASE}/pokemon/{quote(query, safe='')}"
    http = session or requests
    resp = http.get(url, timeout=REQUEST_TIMEOUT)  # TLS verified by default
    if resp.status_code == 404:
        raise PokemonNotFound(f"no Pokemon matching {query!r}")
    resp.raise_for_status()
    return _parse(resp.json())


def _parse(data: dict) -> Pokemon:
    """Read only the fields we expect from the API response."""
    return Pokemon(
        id=int(data["id"]),
        name=str(data["name"]),
        height=int(data["height"]),
        weight=int(data["weight"]),
        types=tuple(t["type"]["name"] for t in data.get("types", [])),
        base_stats={s["stat"]["name"]: int(s["base_stat"]) for s in data.get("stats", [])},
    )
