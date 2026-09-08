# pokedex-secure

**▶ Live demo: https://mechmukul.github.io/pokedex-secure/** (runs in your browser, no install)

A deliberately **security-conscious** Pokedex lookup over the public
[PokeAPI](https://pokeapi.co). The point is not the Pokedex, it is the engineering discipline
around it: validate input before it ever reaches a URL, keep the request safe, and fail without
leaking internals. Available as a **browser tool** (link above) and a **Python CLI**, sharing the
same controls.

![pokedex-secure screenshot](docs/screenshot.png)

## Try it live (20 seconds)
1. Open the live demo link above (it loads Pikachu automatically).
2. Type a Pokemon name or id (e.g. `charizard`, `150`) and **Look up**.
3. Try to break it: `../../etc/passwd`, `http://evil`, or a long junk string. Input is rejected by an allow-list before any request is made.

## Security controls (enforced in both browser and CLI)
| Control | How |
|---|---|
| Allow-list input validation before any request | regex `^[a-z0-9-]{1,50}$` |
| SSRF-safe: fixed API host, user input can't redirect the request | hard-coded base URL |
| Timeouts + TLS never disabled (CLI) | `requests` with timeout, default verify |
| Safe failure: no stack traces or internal URLs leaked | friendly error messages |
| No committed secrets | gitleaks in CI |
| No known-vulnerable dependencies | pip-audit in CI |
| Static analysis on every push | bandit + ruff in CI |

## Run the CLI
```bash
pip install -r requirements.txt
python -m pokedex pikachu
python -m pokedex 25
```

## Run the checks locally
```bash
pip install -r requirements.txt -r requirements-dev.txt
ruff check . && pytest -q && bandit -r pokedex -ll && pip-audit -r requirements.txt
```

See [`SECURITY.md`](SECURITY.md) and the pipeline in `.github/workflows/security.yml`.
Companion to **pokethreatmodel** (the design-level counterpart). Built by Mukul Mech.
