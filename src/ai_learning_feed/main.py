from ai_learning_feed.curation.ranker import CurationEngine
from ai_learning_feed.delivery.telegram import TelegramSender
from ai_learning_feed.harness.agent import LearningAgent
from ai_learning_feed.logging_config import configure_logging
from ai_learning_feed.profile.sample import build_sample_profile

def main():
    """Search for learning resources, curate them, and print the feed."""
    configure_logging()
    profile = build_sample_profile()

    agent = LearningAgent(profile=profile)
    curator = CurationEngine(profile=profile)

    search_results = agent.run("Find recent educational resources about Python.")

    if not search_results:
        raise ValueError("Web search returned no results.")

    feed = curator.curate(
        search_results=search_results,
        limit=profile.daily_content_limit,
    )

    telegram = TelegramSender()
    telegram.send_feed(feed)


if __name__ == "__main__":
    main()
