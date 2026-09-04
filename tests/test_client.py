"""Tests for pokedex.client. Network is mocked; tests run offline in CI."""
from unittest.mock import MagicMock

import pytest

from pokedex.client import (
    InvalidQuery,
    Pokemon,
    PokemonNotFound,
    get_pokemon,
    normalise_query,
)

SAMPLE = {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "types": [{"type": {"name": "electric"}}],
    "stats": [
        {"stat": {"name": "hp"}, "base_stat": 35},
        {"stat": {"name": "speed"}, "base_stat": 90},
    ],
}


@pytest.mark.parametrize("good", ["pikachu", "mr-mime", "25", "ho-oh"])
def test_normalise_accepts_valid(good):
    assert normalise_query(good.upper()) == good.lower()


@pytest.mark.parametrize(
    "bad",
    ["", "a" * 51, "drop table", "../etc/passwd", "pika chu", "http://evil", "réku"],
)
def test_normalise_rejects_injection_and_ssrf(bad):
    with pytest.raises(InvalidQuery):
        normalise_query(bad)


def _mock_session(status=200, payload=None):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = payload or SAMPLE
    resp.raise_for_status = MagicMock()
    session = MagicMock()
    session.get.return_value = resp
    return session


def test_get_pokemon_parses_expected_fields():
    p = get_pokemon("pikachu", session=_mock_session())
    assert isinstance(p, Pokemon)
    assert p.id == 25 and p.name == "pikachu"
    assert p.types == ("electric",)
    assert p.base_stats == {"hp": 35, "speed": 90}


def test_get_pokemon_uses_timeout_and_fixed_host():
    session = _mock_session()
    get_pokemon("25", session=session)
    args, kwargs = session.get.call_args
    assert args[0].startswith("https://pokeapi.co/api/v2/pokemon/")
    assert kwargs.get("timeout")  # timeout must always be set


def test_get_pokemon_404_raises_not_found():
    with pytest.raises(PokemonNotFound):
        get_pokemon("missingno", session=_mock_session(status=404))


def test_invalid_query_never_hits_network():
    session = _mock_session()
    with pytest.raises(InvalidQuery):
        get_pokemon("'; DROP TABLE pokedex;--", session=session)
    session.get.assert_not_called()
