# pokedex-secure

A tiny Pokédex CLI that looks up Pokémon from the public [PokéAPI](https://pokeapi.co) — built
as a portfolio piece to show **how I integrate security into the development lifecycle**. The
code is small; the point is the *engineering discipline* around it.

> Uses only the public PokéAPI. No affiliation with The Pokémon Company.

## Why this exists
An Application Security Engineer's job is not just to find bugs, it is to make the *secure* way
the *default* way. This repo shows secure coding plus a CI pipeline that fails the build on
insecure code, vulnerable dependencies, or committed secrets.

## Usage
```bash
pip install -r requirements.txt
python -m pokedex pikachu
python -m pokedex 25
```

## Security controls (and how they are enforced)
| Control | Enforced by |
|---|---|
| Allow-list input validation before any value reaches a URL | unit tests + ruff `S` |
| SSRF-safe: fixed API host, user input can't redirect the request | code + tests |
| Timeouts always set; TLS never disabled | bandit |
| Defensive parsing (only expected fields read) | code review |
| No secrets committed | gitleaks (CI) |
| No known-vulnerable dependencies | pip-audit (CI) |
| Static analysis on every push/PR | bandit + ruff (CI) |
| Least-privilege CI token | `permissions: contents: read` |

See [`SECURITY.md`](SECURITY.md) and the pipeline in
[`.github/workflows/security.yml`](.github/workflows/security.yml).

## Run the checks locally
```bash
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest -q
bandit -r pokedex -ll
pip-audit -r requirements.txt
```

## Companion repo
See **pokethreatmodel** for a STRIDE threat model of a larger Pokédex system — the design-level
counterpart to this build-level work.
