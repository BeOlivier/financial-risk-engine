# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-07-22

### Added

- Installable `financial-risk-engine` Python distribution using Hatchling.
- Importable `risk_engine` package using a `src/` layout.
- `risk-engine` command-line entry point.
- `version` command.
- `config-check` command for loading and validating runtime TOML configuration.
- Typed runtime configuration for project identity, logging level, and output directory.
- Centralized console logging configured at the CLI application boundary.
- Application-specific configuration exceptions.
- Automated pytest tests with coverage reporting.
- Ruff linting and formatting.
- Strict mypy checking for application source.
- Local pre-commit file-hygiene and Ruff hooks.
- GitHub Actions CI for pull requests and pushes to `main`.
- Hatchling wheel and source-distribution builds.
- Project installation, development, configuration, and roadmap documentation.

### Security and scope

- CI permissions are limited to repository read access.
- No credentials, private datasets, or employer-owned material are included.
- Version `0.1.0` contains the software-engineering foundation only.
- Portfolio calculations and financial risk models are not yet implemented.

### Disclaimer

This release is educational and experimental. It is not validated for
production risk management, regulatory reporting, trading, investment
decisions, or capital allocation.
