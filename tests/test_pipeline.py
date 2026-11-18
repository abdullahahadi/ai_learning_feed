from types import SimpleNamespace

import pytest

from ai_learning_feed.curation.schema import CuratedFeed
from ai_learning_feed.pipeline import curate, deliver, search


def test_search_writes_results_to_output_file(monkeypatch, tmp_path):
    output_path = tmp_path / "nested" / "search_results.txt"
    received = {}

    def make_agent(profile):
        received["profile"] = profile
        return SimpleNamespace(run=lambda query: f"Results for: {query}")

    monkeypatch.setattr(search, "LearningAgent", make_agent)

    search.run_search("Python tutorials", output_path)

    assert output_path.read_text(encoding="utf-8") == "Results for: Python tutorials"
    assert received["profile"].background == "Software Developer"


def test_search_raises_for_empty_results(monkeypatch, tmp_path):
    monkeypatch.setattr(
        search,
        "LearningAgent",
        lambda profile: SimpleNamespace(run=lambda query: ""),
    )

    with pytest.raises(ValueError, match="Web search returned no results"):
        search.run_search("Python tutorials", tmp_path / "search_results.txt")


def test_curation_reads_results_and_writes_feed_json(
    monkeypatch, tmp_path, curated_feed
):
    input_path = tmp_path / "search_results.txt"
    output_path = tmp_path / "curated_feed.json"
    input_path.write_text("sample search results", encoding="utf-8")
    received = {}

    def make_engine(profile):
        def run(search_results, limit):
            received["search_results"] = search_results
            received["limit"] = limit
            return curated_feed

        return SimpleNamespace(curate=run)

    monkeypatch.setattr(curate, "CurationEngine", make_engine)

    curate.run_curation(input_path, output_path)

    assert received["search_results"] == "sample search results"
    assert received["limit"] == 5
    assert CuratedFeed.model_validate_json(output_path.read_text(encoding="utf-8")) == curated_feed


def test_delivery_loads_feed_json_and_sends_it(monkeypatch, tmp_path, curated_feed):
    input_path = tmp_path / "curated_feed.json"
    input_path.write_text(curated_feed.model_dump_json(), encoding="utf-8")
    sent_feeds = []
    monkeypatch.setattr(
        deliver,
        "TelegramSender",
        lambda: SimpleNamespace(send_feed=sent_feeds.append),
    )

    deliver.run_delivery(input_path)

    assert sent_feeds == [curated_feed]
