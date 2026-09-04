"""Command-line interface for pokedex-secure.

Usage:
    python -m pokedex pikachu
    python -m pokedex 25
"""
from __future__ import annotations

import argparse
import sys

import requests

from . import __version__
from .client import InvalidQuery, PokemonNotFound, get_pokemon


def _format(p) -> str:
    stats = "\n".join(f"    {k:<16} {v}" for k, v in p.base_stats.items())
    return (
        f"#{p.id:>4}  {p.name.title()}\n"
        f"  types:  {', '.join(p.types)}\n"
        f"  height: {p.height}   weight: {p.weight}\n"
        f"  base stats:\n{stats}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pokedex", description="Look up a Pokemon by name or id (public PokeAPI)."
    )
    parser.add_argument("query", help="Pokemon name (e.g. pikachu) or id (e.g. 25)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    try:
        pokemon = get_pokemon(args.query)
    except InvalidQuery as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        return 2
    except PokemonNotFound as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except requests.RequestException:
        # Do not leak internal details (URLs, stack traces) to the user.
        print("Could not reach the PokeAPI. Please try again later.", file=sys.stderr)
        return 3

    print(_format(pokemon))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
