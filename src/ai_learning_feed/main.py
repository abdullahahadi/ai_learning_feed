from ai_learning_feed.curation.ranker import CurationEngine
from ai_learning_feed.delivery.telegram import TelegramSender
from ai_learning_feed.harness.agent import LearningAgent
from ai_learning_feed.profile.sample import build_sample_profile


def main():
    """Search for learning resources, curate them, and print the feed."""
    profile = build_sample_profile()

    agent = LearningAgent(profile=profile)
    curator = CurationEngine(profile=profile)

    print("Searching the web...")

    search_results = agent.run("Find recent educational resources about Python.")

    if not search_results:
        raise ValueError("Web search returned no results.")

    print("Search completed.")

    print("Curating content...")

    feed = curator.curate(
        search_results=search_results,
        limit=profile.daily_content_limit,
    )

    print("Sending feed to Telegram...")

    telegram = TelegramSender()
    telegram.send_feed(feed)

    print("Feed delivered successfully!")


if __name__ == "__main__":
    main()
