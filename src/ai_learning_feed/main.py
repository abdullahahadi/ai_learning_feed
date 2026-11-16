from ai_learning_feed.profile.schema import LearningProfile
from ai_learning_feed.harness.agent import LearningAgent
from ai_learning_feed.curation.ranker import CurationEngine
from ai_learning_feed.delivery.telegram import TelegramSender

def main():
    """Search for learning resources, curate them, and print the feed."""
    profile = LearningProfile(
        background="Software Developer",

        interests=[
            "Python",
            "Python project setup",
            "UV",
            "pre-commit",
        ],

        goals=[
            "Become a better Python Developer",
            "Build Python-powered applications",
            "Learn practical Python concepts",
        ],

        current_level={
            "Python": "Intermediate",
            "Python Scripting": "Beginner",
            "Backend Development": "Intermediate",
        },

        preferred_learning_style=[
            "Practical examples",
            "Step-by-step tutorials",
            "Technical articles",
            "YouTube videos"
        ],

        excluded_topics=[],

        daily_content_limit=5,
    )

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
