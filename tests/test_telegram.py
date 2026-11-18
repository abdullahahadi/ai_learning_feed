from unittest.mock import Mock

import pytest
import requests

from ai_learning_feed.delivery.telegram import TelegramSender


def test_sender_requires_credentials(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    with pytest.raises(ValueError, match="Telegram credentials are missing"):
        TelegramSender()


def test_send_message_posts_to_telegram(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "1234")
    response = Mock()
    response.json.return_value = {"ok": True, "result": {"message_id": 1}}
    post = Mock(return_value=response)
    monkeypatch.setattr("ai_learning_feed.delivery.telegram.requests.post", post)
    sender = TelegramSender()

    result = sender.send_message("hello")

    assert result == {"ok": True, "result": {"message_id": 1}}
    post.assert_called_once_with(
        "https://api.telegram.org/bottest-token/sendMessage",
        json={"chat_id": "1234", "text": "hello"},
        timeout=15,
    )
    response.raise_for_status.assert_called_once_with()


def test_send_message_raises_for_telegram_api_error(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "1234")
    response = Mock()
    response.json.return_value = {"ok": False, "description": "Forbidden"}
    monkeypatch.setattr(
        "ai_learning_feed.delivery.telegram.requests.post",
        Mock(return_value=response),
    )

    with pytest.raises(RuntimeError, match="Forbidden"):
        TelegramSender().send_message("hello")


def test_send_message_propagates_http_error(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "1234")
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("bad response")
    monkeypatch.setattr(
        "ai_learning_feed.delivery.telegram.requests.post",
        Mock(return_value=response),
    )

    with pytest.raises(requests.HTTPError, match="bad response"):
        TelegramSender().send_message("hello")


def test_send_feed_sends_header_and_formatted_topics(monkeypatch, curated_feed, curated_topic):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "1234")
    sender = TelegramSender()
    sender.send_message = Mock()

    sender.send_feed(curated_feed)

    assert sender.send_message.call_count == 2
    assert sender.send_message.call_args_list[0].args == (
        "🧠 YOUR AI-CURATED LEARNING FEED\n\n",
    )
    topic_message = sender.send_message.call_args_list[1].args[0]
    assert f"1. {curated_topic.title}" in topic_message
    assert curated_topic.description in topic_message
    assert curated_topic.url in topic_message
    assert "Relevance: 8/10" in topic_message
    assert "Learning value: 9/10" in topic_message
    assert curated_topic.reason_for_recommendation in topic_message
