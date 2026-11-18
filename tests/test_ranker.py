from types import SimpleNamespace

import pytest

from ai_learning_feed.curation import ranker
from ai_learning_feed.curation.schema import CuratedFeed, CuratedTopic


def make_topic(title, relevance, learning_value):
    return CuratedTopic(
        title=title,
        description=f"Description for {title}",
        url=f"https://example.com/{title.lower().replace(' ', '-')}",
        source="Example",
        relevance_score=relevance,
        learning_value=learning_value,
        reason_for_recommendation="Relevant and useful.",
    )


def test_curate_ranks_topics_and_applies_limit(monkeypatch, learning_profile):
    feed = CuratedFeed(
        topics=[
            make_topic("Learning value leader", 6, 10),
            make_topic("Relevance leader", 10, 5),
            make_topic("Low score", 2, 2),
        ]
    )
    captured = {}

    def parse(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(output_parsed=feed)

    monkeypatch.setattr(ranker.client.responses, "parse", parse)

    result = ranker.CurationEngine(learning_profile).curate("search text", limit=2)

    assert [item.title for item in result.topics] == [
        "Relevance leader",
        "Learning value leader",
    ]
    assert "Return no more than 2 topics" in captured["input"]
    assert "search text" in captured["input"]
    assert captured["text_format"] is CuratedFeed


def test_curate_raises_when_response_is_not_parsed(monkeypatch, learning_profile):
    monkeypatch.setattr(
        ranker.client.responses,
        "parse",
        lambda **kwargs: SimpleNamespace(output_parsed=None),
    )

    with pytest.raises(ValueError, match="Could not parse curated feed"):
        ranker.CurationEngine(learning_profile).curate("search text")
