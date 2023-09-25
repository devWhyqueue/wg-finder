import os
from pathlib import Path

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_flat_ad(flat_description):
    template = (Path(__file__).parent / Path("templates/summarize_prompt.txt")).read_text(encoding="UTF-8")
    prompt = template.replace("{DESCRIPTION}", flat_description)
    return _chat_with_gpt(prompt)


def generate_response(flat_description):
    template = (Path(__file__).parent / Path("templates/response_prompt.txt")).read_text(encoding="UTF-8")
    prompt = template.replace("{DESCRIPTION}", flat_description)
    return _chat_with_gpt(prompt)


def generate_creative_response(flat_description):
    template = (Path(__file__).parent / Path("templates/creative_response_prompt.txt")).read_text(encoding="UTF-8")
    prompt = template.replace("{DESCRIPTION}", flat_description)
    return _chat_with_gpt(prompt, engine="gpt-4")


def _chat_with_gpt(prompt, engine="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=engine,
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content
