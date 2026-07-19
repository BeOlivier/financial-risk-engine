"""Application-specific exception types."""


class RiskEngineError(Exception):
    """Base exception for expected financial risk engine failures."""


class ConfigurationError(RiskEngineError):
    """Base exception for runtime configuration failures."""


class ConfigurationFileError(ConfigurationError):
    """Raised when a configuration file cannot be accessed."""


class ConfigurationSyntaxError(ConfigurationError):
    """Raised when a configuration file contains invalid TOML."""


class ConfigurationValidationError(ConfigurationError):
    """Raised when parsed configuration values are invalid."""
