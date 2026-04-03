import configparser
from functools import lru_cache
from pathlib import Path


APP_CONFIG_PATH = Path(__file__).resolve().parent / "config" / "app.ini"
MUST_CHANGE_VALUE = "MUST_CHANGE"


@lru_cache(maxsize=1)
def load_app_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    if not config.read(APP_CONFIG_PATH):
        raise RuntimeError(f"Missing app config file: {APP_CONFIG_PATH}")
    return config


def get_required_config(section: str, option: str, *, allow_placeholder: bool = False) -> str:
    config = load_app_config()
    try:
        value = config[section][option].strip()
    except KeyError as exc:
        raise RuntimeError(
            f"Missing required config value '{section}.{option}' in {APP_CONFIG_PATH}"
        ) from exc

    if not value:
        raise RuntimeError(
            f"Empty required config value '{section}.{option}' in {APP_CONFIG_PATH}"
        )

    if not allow_placeholder and value == MUST_CHANGE_VALUE:
        raise RuntimeError(
            f"Config value '{section}.{option}' in {APP_CONFIG_PATH} must be changed"
        )

    return value
