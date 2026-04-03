import configparser
from functools import lru_cache
from importlib.resources import as_file, files


MUST_CHANGE_VALUE = "MUST_CHANGE"


@lru_cache(maxsize=1)
def load_app_config() -> configparser.ConfigParser:
    """Load and cache the application configuration file."""
    config = configparser.ConfigParser()
    config_resource = files("wgfinder").joinpath("config", "app.ini")
    with as_file(config_resource) as app_config_path:
        if not config.read(app_config_path):
            raise RuntimeError(f"Missing app config file: {app_config_path}")
        return config


def get_required_config(
    section: str, option: str, *, allow_placeholder: bool = False
) -> str:
    """Return a required config value and validate placeholder handling."""
    config = load_app_config()
    try:
        value = config[section][option].strip()
    except KeyError as exc:
        raise RuntimeError(
            f"Missing required config value '{section}.{option}' in app config"
        ) from exc

    if not value:
        raise RuntimeError(
            f"Empty required config value '{section}.{option}' in app config"
        )

    if not allow_placeholder and value == MUST_CHANGE_VALUE:
        raise RuntimeError(
            f"Config value '{section}.{option}' in app config must be changed"
        )

    return value
