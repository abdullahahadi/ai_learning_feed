import argparse
from pathlib import Path

from ai_learning_feed.harness.agent import LearningAgent
from ai_learning_feed.logging_config import configure_logging
from ai_learning_feed.profile.sample import build_sample_profile

DEFAULT_QUERY = "Find recent educational resources about Python."
DEFAULT_OUTPUT = Path("data/search_results.txt")


def run_search(query: str, output_path: Path) -> None:
    """Search for resources and save the raw results as UTF-8 text."""
    profile = build_sample_profile()
    results = LearningAgent(profile).run(query)

    if not results:
        raise ValueError("Web search returned no results.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(results, encoding="utf-8")


def main() -> None:
    configure_logging()
    parser = argparse.ArgumentParser(description="Search for learning resources.")
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    run_search(args.query, args.output)


if __name__ == "__main__":
    main()
