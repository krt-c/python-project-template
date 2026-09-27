# Project instructions

## Purpose

This repository is a generic Python application starter. Replace its example package, metadata, command, and documentation with project-specific choices as the application grows. Do not copy requirements from another project unless they apply here.

## Before changing code

- Read the relevant code and its callers. Keep changes focused and follow existing conventions.
- Use available indexed code navigation first; if it is unavailable or insufficient, use `rg` or another focused search and state that fallback in the handoff.
- Keep compatibility, configuration, and documentation aligned with the requested behavior.
- Before adding a third-party dependency, compare suitable packages with the standard-library or custom-build option. Check current official documentation, compatibility, maintenance, licensing, security, and evidence of real-world use and ratings/reviews. If reliable ratings are unavailable, say so and ask before selecting a package.

## Design

- Keep modules, classes, and functions cohesive. Add abstractions only where they protect policy, support a real variant, or provide a useful test seam.
- Keep business rules separate from delivery frameworks and external services when the application has meaningful policy. Inject infrastructure at the composition root rather than constructing it inside core workflows.
- Use narrow contracts at real boundaries and keep data models separate from service or adapter implementations when that improves clarity.
- Add a concise docstring to each class and function describing its purpose and meaningful inputs, outputs, side effects, or errors.
- Prefer explicit types, conventional formatting, and descriptive names.

## Tests and checks

- Add focused unit tests with behavior changes. Keep ordinary tests deterministic and offline; use fakes and fixtures for external boundaries.
- Mark real network, model, or service smoke tests as opt-in. Do not make them part of the default test run.
- Run relevant checks when requested or needed to verify an authorized change. Report commands and outcomes accurately.
- Recommended local checks are listed in `README.md` and configured in `pyproject.toml`.

## Git safeguards

- Do not create, amend, rewrite, or push commits unless the user explicitly requests that specific action.
- Do not create a pull request unless the user explicitly requests it.
- Keep secrets out of source, fixtures, logs, and committed configuration. `.env.example` contains placeholders only.
