import argparse
from pathlib import Path

from ai_learning_feed.curation.schema import CuratedFeed
from ai_learning_feed.delivery.telegram import TelegramSender

DEFAULT_INPUT = Path("data/curated_feed.json")


def run_delivery(input_path: Path) -> None:
    """Load a curated feed from JSON and send it to Telegram."""
    feed = CuratedFeed.model_validate_json(input_path.read_text(encoding="utf-8"))
    TelegramSender().send_feed(feed)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a curated feed to Telegram.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args()
    run_delivery(args.input)


if __name__ == "__main__":
    main()
