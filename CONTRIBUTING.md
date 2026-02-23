# Contributing to esiosapy

Thank you for your interest in contributing to esiosapy! This guide will help you get started.

## Development setup

### Prerequisites

- Python 3.9 or higher
- [uv](https://docs.astral.sh/uv/) for dependency management

### Getting started

1. Fork and clone the repository:

```bash
git clone https://github.com/<your-username>/esiosapy.git
cd esiosapy
```

2. Install dependencies:

```bash
uv sync
```

This will install all development and test dependencies.

## Development workflow

### Running checks

Before submitting any changes, make sure all checks pass:

```bash
# Format code
uv run ruff format esiosapy/ tests/

# Lint code
uv run ruff check esiosapy/ tests/

# Type check
uv run mypy esiosapy/ tests/

# Run tests
uv run pytest tests/
```

### Code style

- **Formatter**: [ruff](https://docs.astral.sh/ruff/) with a line length of 88
- **Type checking**: [mypy](https://mypy-lang.org/) in strict mode
- All files must include `from __future__ import annotations`
- Absolute imports only (no relative imports)

### Commit conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/). Your commit messages should be structured as:

```
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

Common types:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring without behavior changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks

Examples:

```
feat: add pagination support to indicator listing
fix: handle empty response from archives endpoint
docs: update installation instructions in README
test: add tests for async client error handling
```

### Branching model

- `master`: Production-ready releases
- `develop`: Integration branch for new features
- Feature branches should be created from `develop`

## Pull request process

1. Create a feature branch from `develop`:

```bash
git checkout develop
git checkout -b feat/my-feature
```

2. Make your changes and ensure all checks pass.
3. Push your branch and open a pull request targeting `develop`.
4. Provide a clear description of your changes in the PR.

## Reporting issues

If you find a bug or have a feature request, please [open an issue](https://github.com/M4RC0Sx/esiosapy/issues) with as much detail as possible.
