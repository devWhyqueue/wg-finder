from importlib.resources import files

import backoff
from openai import OpenAI

from wgfinder.app_config import get_required_config
from wgfinder.models import FlatAd


def _get_client() -> OpenAI:
    return OpenAI(api_key=get_required_config("openai", "api_key"))


def _get_model_config(option: str) -> str:
    """Return the configured model name for the requested OpenAI task."""
    return get_required_config("openai", option)


def summarize_flat_ad(flat_ad: FlatAd | str) -> str:
    """Summarize a flat listing so it can be reviewed quickly."""
    template = _load_template("summarize_prompt.txt")
    flat_ad_text = flat_ad.to_string() if isinstance(flat_ad, FlatAd) else flat_ad
    prompt = template.replace("{FLAT_AD}", flat_ad_text)
    return _chat_with_gpt(prompt, engine=_get_model_config("summary_model"))


def generate_response(flat_ad: FlatAd) -> str:
    """Generate an application message for a flat listing."""
    system_prompt = _load_config_text("system_prompt.txt")
    user_prompt = f"# WG-Inserat\n\n{flat_ad.to_string()}"
    return _chat_with_gpt(
        user_prompt,
        system_prompt,
        engine=_get_model_config("response_model"),
    )


@backoff.on_exception(backoff.expo, Exception)
def _chat_with_gpt(
    user_prompt: str, system_prompt: str = "", engine: str = "gpt-5-mini"
) -> str:
    response = _get_client().responses.create(
        model=engine,
        instructions=system_prompt or None,
        input=user_prompt,
    )
    content = response.output_text.strip()
    if not content:
        raise RuntimeError(f"OpenAI response for model '{engine}' was empty")
    return content


def _load_template(template_name: str) -> str:
    return (
        files("wgfinder")
        .joinpath("templates", template_name)
        .read_text(encoding="utf-8")
    )


def _load_config_text(file_name: str) -> str:
    return files("wgfinder").joinpath("config", file_name).read_text(encoding="utf-8")
