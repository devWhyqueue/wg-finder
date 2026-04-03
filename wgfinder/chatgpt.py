from pathlib import Path

import backoff
from openai import OpenAI

from wgfinder.app_config import get_required_config


def _get_client() -> OpenAI:
    return OpenAI(api_key=get_required_config("openai", "api_key"))


def summarize_flat_ad(flat_ad):
    template = (
        Path(__file__).parent / Path("templates/summarize_prompt.txt")
    ).read_text(encoding="UTF-8")
    prompt = template.replace("{FLAT_AD}", flat_ad.to_string())
    return _chat_with_gpt(prompt)


def generate_response(flat_ad):
    system_prompt = (
        Path(__file__).parent / Path("templates/system_prompt.txt")
    ).read_text(encoding="UTF-8")
    user_prompt = f"# WG-Inserat\n\n{flat_ad.to_string()}"
    return _chat_with_gpt(user_prompt, system_prompt, engine="gpt-5")


@backoff.on_exception(backoff.expo, Exception)
def _chat_with_gpt(user_prompt, system_prompt="", engine="gpt-5-mini"):
    response = _get_client().chat.completions.create(
        model=engine,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content
