import argparse
from pathlib import Path

from ai_learning_feed.curation.ranker import CurationEngine
from ai_learning_feed.logging_config import configure_logging
from ai_learning_feed.profile.sample import build_sample_profile

DEFAULT_INPUT = Path("data/search_results.txt")
DEFAULT_OUTPUT = Path("data/curated_feed.json")


def run_curation(input_path: Path, output_path: Path) -> None:
    """Curate search-result text and save the structured feed as JSON."""
    profile = build_sample_profile()
    search_results = input_path.read_text(encoding="utf-8")
    feed = CurationEngine(profile).curate(
        search_results=search_results,
        limit=profile.daily_content_limit,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(feed.model_dump_json(indent=2), encoding="utf-8")


def main() -> None:
    configure_logging()
    parser = argparse.ArgumentParser(description="Curate search results into a feed.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    run_curation(args.input, args.output)


if __name__ == "__main__":
    main()
