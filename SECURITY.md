# Security policy

## Reporting a vulnerability
Please open a private security advisory on this repository, or email the maintainer. Do not
open a public issue for a suspected vulnerability. I aim to acknowledge within 72 hours.

## Security controls in this project
This is a deliberately small tool, but it is built the way production code should be.

| Control | Where | Enforced by |
|---|---|---|
| Input validation (allow-list) | `pokedex/client.py` `normalise_query` | Unit tests + ruff `S` rules |
| SSRF-safe: fixed API host, no user-controlled URL | `client.py` `API_BASE` | Code review + tests |
| Request timeouts always set | `client.py` `REQUEST_TIMEOUT` | bandit (B113) |
| TLS verification never disabled | `client.py` (default `verify=True`) | bandit + code review |
| No secrets in code or logs | whole repo | gitleaks in CI |
| Dependency vulnerabilities | `requirements.txt` | pip-audit in CI |
| Static analysis | `pokedex/` | bandit + ruff in CI |
| Least privilege in CI | `.github/workflows/security.yml` | `permissions: contents: read` |

## Supported versions
The latest `main` is supported.
