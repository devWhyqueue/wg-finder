from pathlib import Path

import backoff
from openai import OpenAI

client = OpenAI()


def summarize_flat_ad(flat_description):
    template = (Path(__file__).parent / Path("templates/summarize_prompt.txt")).read_text(encoding="UTF-8")
    prompt = template.replace("{DESCRIPTION}", flat_description)
    return _chat_with_gpt(prompt)


def generate_response(flat_description):
    system_prompt = (Path(__file__).parent / Path("templates/system_prompt.txt")).read_text(encoding="UTF-8")
    user_prompt = f"# WG-Inserat\n\n{flat_description}"
    return _chat_with_gpt(user_prompt, system_prompt, engine="gpt-5")


@backoff.on_exception(backoff.expo, Exception)
def _chat_with_gpt(user_prompt, system_prompt="", engine="gpt-5-mini"):
    response = client.chat.completions.create(
        model=engine,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    
    return response.choices[0].message.content
