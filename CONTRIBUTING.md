# Contributing Guide

Thank you for your interest in contributing to ASCIA! This guide outlines expectations for code quality, testing, documentation, and governance so that every change is production-ready.

## Development Workflow
1. Fork and clone the repository.
2. Create a feature branch (`git checkout -b feature/my-change`).
3. Install dependencies with `pip install -e .[dev]` and ensure `python -m venv .venv` is activated.
4. Run `ruff check .` and `pytest` locally; fix all warnings before opening a PR.
5. Submit a pull request that describes the change, risk considerations, and how to validate.

## Code Standards
- Follow PEP 8, include type hints, and keep functions small and purposeful.
- Add docstrings for all public classes and functions, explaining *why* complex logic exists.
- Include structured logging for meaningful operations and errors.
- Validate inputs and avoid hard-coded secrets; use configuration or environment variables where appropriate.
- Keep simulations clearly separated from real environments to avoid unintended cloud interactions.

## Security Expectations
- Never commit credentials, tokens, or live cloud endpoints.
- Prefer parameterized data handling and validate untrusted inputs to avoid injection risks.
- Report vulnerabilities privately to `security@ascia.example.com` before opening a public issue.

## Tests
- Add or update unit tests for new functionality with deterministic assertions.
- Use fixtures for mock data and prefer fast-running tests over integration-style tests.
- Maintain coverage over remediation logic, validation, and connectors.

## Documentation
- Update README and relevant docs (e.g., `docs/API.md`, `docs/ARCHITECTURE.md`, `docs/OPERATIONS.md`) for user-facing changes.
- Include usage examples when adding endpoints, CLI tools, or dashboards.
- Keep diagrams and data flows current.

## Release Hygiene
- Ensure CI passes and changelog entries (if introduced) are updated.
- When modifying IaC generation, verify new files land under `iac_versions/` with safe defaults.
- Keep log statements free of sensitive data while providing enough detail for troubleshooting.
