from types import SimpleNamespace

import pytest

from wgfinder import chatgpt
from wgfinder.models import FlatAd

flat_description = (
    "Hallo ihr Suchenden,\n\n"
    "unsere liebe Mitbewohnerin zieht mit ihrem Freund in eine eigene Wohnung, somit wird das Zimmer frei.\n\n"
    "Nichtraucherwohnung, Altbau, hohe Decken, Erdgeschoss - EG, ruhige Seitenstraße.\n\n"
    "Möbliert, Hochbett, Schreibtisch, Stühle, 2-er Sofa, Sessel, Kleiderschrank, Kommode.\n"
    "Kann man alles benutzen oder ihr bringt komplett eigene Möbel mit, dann kommen die hier vorhandenen Möbel weg.\n\n"
    "Anmeldung natürlich möglich.\n\n"
    "Sonst alles da, Wasch- u. Spülmaschine, voll eingerichtete Küche usw.\n\n"
    "Liebe Grüße,\n"
    "Tom\n"
    "----------------------------------------------------------------------------------------------------------------------\n"
    "ENGLISH\n\n"
    "Hi guys,\n\n"
    "our dear flatmate moves into an own appartement together with her boyfriend, so the room is free.\n\n"
    "ONLY for grown up, responsible people who know how to run a household and keep the bathroom and kitchen clean. "
    "If you can´t do that, you´re very wrong here.\n\n"
    "Non-smoker flat. \"Altbau\" = apartment in old building. Flat is on the ground floor. House is in a smal, quiet street, "
    "has a big bathroom and kitchen.\n"
    "Of course you can use the washing-machine and kitchen etc.\n\n"
    "Yes, you can get a tenancy/sublease (Untermietvertrag) and a \"Anmeldung\" = registration.\n\n"
    "There´s furniture like a bed, desk, wardrobe (closet), some chairs, sofa/couch, if you need it. "
    "If not, you can bring your own furniture, then the furniture from this room will be removed.\n\n"
    "Good connection to public transport.\n\n"
    "I´m a cinematographer and photographer, I like to do some sports (no fitnessfreak), play some piano - "
    "but at home only E-Piano with headphones, so you don´t hear anything. Your other flatmate would be a very open minded IT-guy, "
    "very communicative an interested in many things.\n\n"
    "Great if you already have experience with living in a shared-flat.\n\n"
    "We have a relaxed life here, sometimes we talk/eat/drink together in the kitchen. Or not, then we chill or work alone in our own room. "
    "There´s no \"must\" for anything.\n\n"
    "Späti (late-shop) and supermarket 3 min. away.\n"
    "Public transport:\n"
    "ca. 3 min to tram (50, M13).\n"
    "ca. 4 min to S-Bahn Bornholmer Straße (S1, S2, S25, S26, S8, S85)\n"
    "ca. 12 min to U/S-Bahn (subway) Schönhauser Allee (U2, S8, Ringbahn S41, S42)\n\n"
    "Best,\n"
    "Tom"
)


def _build_flat_ad() -> FlatAd:
    return FlatAd(
        "https://example.com/ad",
        2,
        750,
        24,
        "Neukoelln",
        "2026-04-01",
        flat_description,
        "Alice",
    )


def test_summarize_flat_ad(monkeypatch):
    monkeypatch.setattr(chatgpt, "_get_model_config", lambda option: "gpt-5-mini")
    monkeypatch.setattr(chatgpt, "_chat_with_gpt", lambda prompt, *_args, **_kwargs: "summary")

    response = chatgpt.summarize_flat_ad(_build_flat_ad())

    assert response == "summary"


def test_generate_response_uses_configured_model(monkeypatch):
    captured = {}

    def fake_chat(user_prompt, system_prompt="", engine="gpt-5-mini"):
        captured["user_prompt"] = user_prompt
        captured["system_prompt"] = system_prompt
        captured["engine"] = engine
        return "response"

    monkeypatch.setattr(
        chatgpt,
        "_get_model_config",
        lambda option: {
            "summary_model": "gpt-5-mini",
            "response_model": "gpt-5",
        }[option],
    )
    monkeypatch.setattr(chatgpt, "_chat_with_gpt", fake_chat)

    response = chatgpt.generate_response(_build_flat_ad())

    assert response == "response"
    assert captured["engine"] == "gpt-5"
    assert "# WG-Inserat" in captured["user_prompt"]
    assert captured["system_prompt"]


def test_summarize_flat_ad_uses_configured_model(monkeypatch):
    captured = {}

    def fake_chat(user_prompt, system_prompt="", engine="gpt-5-mini"):
        captured["engine"] = engine
        return "summary"

    monkeypatch.setattr(chatgpt, "_get_model_config", lambda option: "gpt-5-mini")
    monkeypatch.setattr(chatgpt, "_chat_with_gpt", fake_chat)

    response = chatgpt.summarize_flat_ad(_build_flat_ad())

    assert response == "summary"
    assert captured["engine"] == "gpt-5-mini"


def test_chat_with_gpt_uses_responses_api(monkeypatch):
    responses = SimpleNamespace(create=lambda **_kwargs: SimpleNamespace(output_text="summary"))
    monkeypatch.setattr(chatgpt, "_get_client", lambda: SimpleNamespace(responses=responses))

    response = chatgpt._chat_with_gpt("user prompt", "system prompt", "gpt-5-mini")

    assert response == "summary"


def test_chat_with_gpt_rejects_empty_response(monkeypatch):
    responses = SimpleNamespace(create=lambda **_kwargs: SimpleNamespace(output_text=""))
    monkeypatch.setattr(chatgpt, "_get_client", lambda: SimpleNamespace(responses=responses))
    raw_chat_with_gpt = getattr(chatgpt._chat_with_gpt, "__wrapped__", chatgpt._chat_with_gpt)

    with pytest.raises(RuntimeError, match="empty"):
        raw_chat_with_gpt("user prompt")
