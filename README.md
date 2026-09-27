# Python Project Starter

A small, runnable Python project template with a `src/` package, unit and integration test folders, locked `uv` dependencies, static checks, and Docker support.

The starter command prints a greeting so a clean checkout can be installed and run immediately. Replace `starter_app` and `starter-app` with your package and command names when creating a project.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) for the recommended setup
- Node.js 24 and npm for Pyright
- Docker with Compose for container use

## Set up

```powershell
uv sync --locked --extra dev
```

Run the starter app:

```powershell
uv run starter-app
uv run python -m starter_app
```

For a pip-based environment, create and activate a virtual environment, then run:

```text
python -m pip install -e ".[dev]"
starter-app
```

Pyright is managed through npm so its official Node.js distribution is used. On Windows PowerShell, install its locked version with `npm.cmd ci`; on macOS/Linux, use `npm ci`.

## Checks

```powershell
uv run --locked --extra dev pytest
uv run --locked --extra dev ruff check .
uv run --locked --extra dev ruff format --check .
npm.cmd exec -- pyright
uv build
```

On macOS/Linux, use `npm exec -- pyright` for the type check.

Tests are local and deterministic. Keep network or service smoke tests separately marked and opt-in.

## Docker

Build and run the one-shot starter command:

```powershell
docker compose build
docker compose run --rm app
```

The image runs as a non-root user and installs only locked runtime dependencies. For a web service or worker, update the image command, Compose ports, and health check to match that application.

## Customize for a new project

1. Rename `src/starter_app/` and update the imports and module command.
2. Update the project name, description, Python support range, and console script in `pyproject.toml`.
3. Update the `starter-app` command in `Dockerfile`, tests, and documentation.
4. Regenerate `uv.lock` with `uv lock` after changing dependencies or project metadata; regenerate `package-lock.json` after changing `package.json`.
5. Keep tests under `tests/unit/` and `tests/integration/`. Use fakes and fixtures for ordinary tests.
6. Add application-specific configuration to `.env.example`; Compose reads a copied `.env` file for interpolation, while the Python app does not load `.env` automatically. Keep `.env` values and credentials out of Git.

Small projects can keep a simple package structure. Add subpackages for domain rules, application workflows, external adapters, presentation, or dependency wiring only when those boundaries help the project.
