# financial-risk-engine

[![CI](https://github.com/BeOlivier/financial-risk-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/BeOlivier/financial-risk-engine/actions/workflows/ci.yml)

A Python project for building financial-risk and portfolio-analysis tools
with reproducible configuration, automated testing, static analysis, and
continuous integration.

## Project status

Early development.

Version `0.1.0` establishes the project foundation:

- installable Python package;
- command-line interface;
- TOML runtime configuration;
- structured console logging;
- automated tests and coverage reporting;
- Ruff linting and formatting;
- mypy static type checking;
- pre-commit hooks;
- GitHub Actions continuous integration;
- Hatchling package builds.

Financial risk calculations and portfolio-analysis models are planned for
later versions and are not yet implemented.

## Project naming

The project uses different names in different contexts:

| Context | Name | Purpose |
|---|---|---|
| GitHub repository | `financial-risk-engine` | Repository and project name |
| Python distribution | `financial-risk-engine` | Name used by pip and package metadata |
| Python package | `risk_engine` | Name used in Python imports |
| Terminal command | `risk-engine` | Command installed into the active environment |

Examples:

```python
import risk_engine

print(risk_engine.__version__)
```

```bash
risk-engine version
```

## Requirements

- Python `3.14` or later
- Git
- pip

Development has been verified with Python `3.14.6`.

## Installation

Clone the repository:

```bash
git clone https://github.com/BeOlivier/financial-risk-engine.git
cd financial-risk-engine
```

Create a virtual environment:

```bash
python3.14 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the package and development tools:

```bash
python -m pip install -e ".[dev]"
```

The editable installation links the installed package to the source files in
the repository. Changes under `src/risk_engine/` are therefore available
without reinstalling the project after every code edit.

The `dev` extra installs the development tools used by this repository,
including pytest, pytest-cov, Ruff, mypy, pre-commit, and build.

## Usage

Display the available commands:

```bash
risk-engine --help
```

Display the installed version:

```bash
risk-engine version
```

Expected output:

```text
risk-engine 0.1.0
```

Validate and summarize a runtime configuration:

```bash
risk-engine config-check --config configs/example.toml
```

Expected output:

```text
Configuration is valid: configs/example.toml
Project: Example Portfolio Analysis
Logging level: INFO
Output directory: outputs
```

The package can also be executed through Python:

```bash
python -m risk_engine --help
python -m risk_engine version
python -m risk_engine config-check --config configs/example.toml
```

Both invocation forms use the same command-line implementation:

```text
risk-engine
python -m risk_engine
```

## Runtime configuration

Runtime configuration controls settings for a particular application run.

It is separate from `pyproject.toml`:

- `pyproject.toml` defines packaging, dependencies, tool settings, and build
  metadata.
- Files under `configs/` define settings used while running the application.

Example:

```toml
[project]
name = "Example Portfolio Analysis"

[logging]
level = "INFO"

[output]
directory = "outputs"
```

### `project.name`

Required.

A non-empty string identifying the analysis or portfolio.

### `logging.level`

Optional.

Default:

```text
INFO
```

Supported values:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Logging levels are case-insensitive and are normalized to uppercase.

### `output.directory`

Optional.

Default:

```text
outputs
```

The value is validated and represented as a filesystem path. Version `0.1.0`
does not yet generate portfolio reports or financial-model outputs.

## Development

Run the automated tests:

```bash
python -m pytest
```

The test command also produces a coverage report because coverage options are
configured in `pyproject.toml`.

Run Ruff linting:

```bash
ruff check .
```

Apply safe Ruff fixes:

```bash
ruff check . --fix
```

Check Python formatting:

```bash
ruff format --check .
```

Apply Python formatting:

```bash
ruff format .
```

Run static type checking:

```bash
mypy src/risk_engine
```

Run all local pre-commit hooks:

```bash
pre-commit run --all-files
```

Install the local Git pre-commit hook:

```bash
pre-commit install
```

Build the wheel and source distribution:

```bash
python -m build
```

Build artifacts are created under:

```text
dist/
```

## Continuous integration

GitHub Actions runs the CI workflow automatically for:

- pull requests targeting `main`;
- pushes to `main`;
- manual workflow dispatches.

The workflow currently verifies:

- pre-commit hooks;
- Ruff formatting;
- Ruff linting;
- mypy static checking;
- pytest tests and coverage;
- package builds;
- CLI version execution;
- example configuration validation.

## Roadmap

Planned development stages:

- `v0.1` — package foundation, CLI, configuration, logging, tests, and CI;
- `v0.2` — portfolio data loading and return calculations;
- `v0.3` — portfolio statistics and risk metrics;
- `v0.4` — Value at Risk models;
- `v0.5` — Expected Shortfall and model comparison;
- `v0.6` — Monte Carlo simulation;
- `v0.7` — stress testing and scenario analysis;
- `v0.8` — portfolio analytics and reporting;
- `v0.9` — portfolio optimization;
- `v1.0` — documented and usable initial release.

Roadmap details may change as the financial models and user workflows are
validated.

## License

This project is licensed under the MIT License. See `LICENSE`.

## Disclaimer

This project is intended for education, experimentation, and portfolio
demonstration.

It is not financial advice and has not been independently validated for
production risk management, regulatory reporting, trading, investment
decisions, or capital allocation.

Users must independently verify all calculations, assumptions, data inputs,
and model limitations before relying on any result.
