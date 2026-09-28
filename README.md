# Python Project Starter

A small, runnable Python project template with a Clean Architecture package scaffold, unit and integration test folders, locked `uv` dependencies, static checks, and Docker support.

The `starter-app` command prints a greeting. To initialize a project with consistent package, command, Docker, and documentation names, run:

```powershell
uv run python -m scripts.init_project --name "Example Project"
```

Pass `--dry-run` to preview the changes before writing them.
The name may contain letters and numbers separated by single spaces, hyphens, or underscores, and must start with a letter.

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

Tests are local and deterministic. `@pytest.mark.live` labels tests that contact a real external service; `uv run --locked --extra dev pytest -m live` selects those tests. The marker alone does not exclude them from the default `pytest` run.

## Continuous integration

GitHub Actions runs the tests, Ruff checks, Pyright, and package build on the minimum supported Python version and a newer version. It also installs the package in editable mode with pip and runs the tests again. Adjust the CI version matrix when the project's supported Python range changes.

## Docker

Build and run the one-shot starter command:

```powershell
docker compose build
docker compose run --rm app
```

The image runs as a non-root user and installs only locked runtime dependencies. For a web service or worker, update the image command, Compose ports, and health check to match that application.

## Source package structure

The initializer renames the package under `src/`; its layers are already scaffolded:

```text
src/starter_app/
├── domain/          # Core rules and models; no framework or external-service imports
├── application/     # Use cases and the inward-facing contracts they need
├── infrastructure/  # Database, network, filesystem, and other external adapters
├── presentation/    # CLI, web, and other input/output adapters
└── bootstrap/       # Composition roots that wire adapters to use cases
```

Dependencies point inward: presentation and infrastructure may depend on application and domain; application may depend on domain; domain stays independent. Put concrete wiring in `bootstrap`. Keep the scaffold small and add modules only when the project needs them.

## Agent guidance

`AGENTS.md` contains repository-wide instructions for coding agents. The reusable skills in `.agents/skills/` provide focused guidance on Clean Architecture and SOLID; use them when the change involves meaningful architecture or design decisions. The initializer leaves these files in place for the new project.

## Customize for a new project

1. Run the project initializer before adding application code.
2. Update the description and Python support range in `pyproject.toml` as needed.
3. Add dependencies with `uv add`; regenerate the lockfile with `uv lock` after changing metadata or dependencies.
4. Keep tests under `tests/unit/` and `tests/integration/`. Use fakes and fixtures for ordinary tests.
5. Add application-specific configuration to `.env.example`; Compose reads a copied `.env` file for interpolation, while the Python app does not load `.env` automatically. Keep `.env` values and credentials out of Git.

The starter includes the five layer packages. Add modules within them as the project needs them; avoid adding extra layers or abstractions without a clear responsibility.
