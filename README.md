# financial-risk-engine

[![CI](https://github.com/BeOlivier/financial-risk-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/BeOlivier/financial-risk-engine/actions/workflows/ci.yml)

Portfolio analytics and financial risk modelling toolkit.

## Runtime configuration

The application uses TOML files for settings that may differ between
analysis runs.

Runtime configuration is separate from `pyproject.toml`:

- `pyproject.toml` defines how the Python project is built, installed,
  tested, and packaged.
- Files under `configs/` define settings used while running the
  application.

Example:

```toml
[project]
name = "Example Portfolio Analysis"

[logging]
level = "INFO"

[output]
directory = "outputs"
```

### Settings

#### `project.name`

Required string identifying the analysis or portfolio.

#### `logging.level`

Optional logging level. The default is `INFO`.

Supported values:

- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

Values are case-insensitive.

#### `output.directory`

Optional directory for generated outputs. The default is `outputs`.

Validate a configuration with:

```bash
risk-engine config-check --config configs/example.toml
```

Example output:

```text
Configuration is valid: configs/example.toml
Project: Example Portfolio Analysis
Logging level: INFO
Output directory: outputs
```
