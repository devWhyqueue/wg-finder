import configparser
from functools import lru_cache
from importlib.resources import as_file, files
import os

from dotenv import load_dotenv


MUST_CHANGE_VALUE = "MUST_CHANGE"
SECRET_ENV_VARS = {
    ("webshare", "proxy_url"): "WEBSHARE_PROXY_URL",
    ("openai", "api_key"): "OPENAI_API_KEY",
    ("telegram", "bot_token"): "TELEGRAM_BOT_TOKEN",
    ("telegram", "chat_id"): "TELEGRAM_CHAT_ID",
}


@lru_cache(maxsize=1)
def load_app_config() -> configparser.ConfigParser:
    """Load and cache the application configuration file."""
    load_dotenv()
    config = configparser.ConfigParser(interpolation=None)
    config_resource = files("wgfinder").joinpath("config", "app.ini")
    with as_file(config_resource) as app_config_path:
        if not config.read(app_config_path):
            raise RuntimeError(f"Missing app config file: {app_config_path}")
        return config


def _get_env_value(section: str, option: str) -> tuple[str, str] | None:
    """Return a secret config value from the environment when configured."""
    env_var_name = SECRET_ENV_VARS.get((section, option))
    if not env_var_name:
        return None

    load_dotenv()
    return os.getenv(env_var_name, "").strip(), f"environment variable '{env_var_name}'"


def _get_app_config_value(section: str, option: str) -> tuple[str, str]:
    """Return a config value from app.ini."""
    config = load_app_config()
    try:
        value = config[section][option].strip()
    except KeyError as exc:
        raise RuntimeError(
            f"Missing required config value '{section}.{option}' in app config"
        ) from exc
    return value, "app config"


def get_required_config(
    section: str, option: str, *, allow_placeholder: bool = False
) -> str:
    """Return a required config value and validate placeholder handling."""
    env_value = _get_env_value(section, option)
    value, source = env_value or _get_app_config_value(section, option)

    if not value:
        raise RuntimeError(
            f"Empty required config value '{section}.{option}' in {source}"
        )

    if not allow_placeholder and value == MUST_CHANGE_VALUE:
        raise RuntimeError(
            f"Config value '{section}.{option}' in {source} must be changed"
        )

    return value
