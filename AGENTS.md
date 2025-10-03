# Repository Guidelines

Welcome to the claude-automatic-sniffle project. The repository currently contains only scaffolding, so these guidelines describe how to stage incoming Python packages and keep the codebase coherent as it grows.

## Project Structure & Module Organization
- Place executable or library code under `src/claude_automatic_sniffle/`.
- Keep integration and unit tests under `tests/` mirroring the module tree (e.g., `src/.../foo.py` -> `tests/.../test_foo.py`).
- Store shared fixtures in `tests/conftest.py` and sample assets in `tests/data/`.
- Add documentation drafts or design notes in `docs/` and mark architectural decisions in `docs/adr-YYYYMMDD-topic.md`.

## Build, Test, and Development Commands
- Create a virtual environment once: `python -m venv .venv && source .venv/bin/activate`.
- Install development dependencies: `pip install -r requirements-dev.txt` (add the file when tooling is chosen).
- Run the package locally with `python -m claude_automatic_sniffle` when an entrypoint exists.
- Execute quality gates via `make lint test` or `tox` once the corresponding configs are committed; update this section as commands solidify.

## Coding Style & Naming Conventions
- Use 4-space indentation, type annotations, and docstrings for public functions.
- Format with `black` and lint with `ruff`; configure both in `pyproject.toml`.
- Name modules with lowercase underscores, classes in PascalCase, and functions/variables in snake_case.

## Testing Guidelines
- Target pytest for unit and integration coverage; ensure every feature PR adds or updates tests.
- Name test files `test_<feature>.py` and test functions `def test_behavior_*`.
- Run `pytest --maxfail=1 --disable-warnings --cov=claude_automatic_sniffle` before opening a PR; include coverage reports for substantial changes.

## Commit & Pull Request Guidelines
- Follow Conventional Commits (e.g., `feat: add dataset loader`) to keep history searchable.
- Squash work-in-progress commits; ensure every commit passes lint and tests locally.
- Pull requests should link to related issues, outline testing performed, and attach screenshots or logs for user-facing changes.
- Request at least one review and respond to all feedback before merging.

## Environment & Security Notes
- Keep secrets out of version control; store local overrides in `.env` and document required variables in `.env.example`.
- Rotate API keys regularly and record configuration expectations in `docs/configuration.md`.
