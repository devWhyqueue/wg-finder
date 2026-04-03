from datetime import datetime
import configparser
from unittest.mock import Mock

import pytest

from wgfinder import app_config
from wgfinder import messenger
from wgfinder.models import FlatAd


def _build_flat_ad() -> FlatAd:
    flat_ad = FlatAd(
        "https://example.com/ad",
        2,
        750,
        24,
        "Neukoelln",
        datetime(2026, 4, 1),
        "Nice room",
        "Alice",
    )
    flat_ad.desc_summary = "Bright room near transport."
    flat_ad.response = "Hi, I would love to introduce myself."
    return flat_ad


def test_notify_by_telegram_sends_two_messages(monkeypatch):
    post = Mock()
    post.return_value.raise_for_status = Mock()
    monkeypatch.setattr(messenger.requests, "post", post)
    monkeypatch.setattr(
        messenger,
        "get_required_config",
        lambda section, option: {
            ("telegram", "bot_token"): "bot-token",
            ("telegram", "chat_id"): "123456",
        }[(section, option)],
    )

    flat_ad = _build_flat_ad()

    messenger.notify_by_telegram(flat_ad)

    assert post.call_count == 2
    assert post.call_args_list[0].args[0] == "https://api.telegram.org/botbot-token/sendMessage"
    assert post.call_args_list[0].kwargs["json"]["chat_id"] == "123456"
    assert "Bright room near transport." in post.call_args_list[0].kwargs["json"]["text"]
    assert post.call_args_list[1].kwargs["json"]["text"] == flat_ad.response


def test_notify_by_telegram_raises_for_http_errors(monkeypatch):
    post = Mock()
    post.return_value.raise_for_status.side_effect = RuntimeError("telegram failed")
    monkeypatch.setattr(messenger.requests, "post", post)
    monkeypatch.setattr(
        messenger,
        "get_required_config",
        lambda section, option: {
            ("telegram", "bot_token"): "bot-token",
            ("telegram", "chat_id"): "123456",
        }[(section, option)],
    )

    with pytest.raises(RuntimeError, match="telegram failed"):
        messenger.notify_by_telegram(_build_flat_ad())


def test_get_required_config_rejects_missing_telegram_chat_id(monkeypatch):
    config = configparser.ConfigParser()
    config["telegram"] = {"bot_token": "bot-token"}
    monkeypatch.setattr(app_config, "load_app_config", lambda: config)

    with pytest.raises(RuntimeError, match="telegram.chat_id"):
        app_config.get_required_config("telegram", "chat_id")


def test_get_required_config_rejects_placeholder_telegram_bot_token(monkeypatch):
    config = configparser.ConfigParser()
    config["telegram"] = {
        "bot_token": "MUST_CHANGE",
        "chat_id": "123456",
    }
    monkeypatch.setattr(app_config, "load_app_config", lambda: config)

    with pytest.raises(RuntimeError, match="telegram.bot_token"):
        app_config.get_required_config("telegram", "bot_token")
