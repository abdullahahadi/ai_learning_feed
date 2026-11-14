from app.profile.schema import LearningProfile
from app.harness.agent import LearningAgent
from app.curation.ranker import CurationEngine
from app.delivery.telegram import TelegramSender

def main():
    """Search for learning resources, curate them, and print the feed."""
    profile = LearningProfile(
        background="Software Developer",

        interests=[
            "AI Engineering",
            "Python",
            "Backend Development",
            "Data Engineering",
        ],

        goals=[
            "Become a better AI Engineer",
            "Build AI-powered applications",
            "Learn practical AI concepts",
        ],

        current_level={
            "Python": "Intermediate",
            "AI Engineering": "Beginner",
            "Backend Development": "Intermediate",
        },

        preferred_learning_style=[
            "Practical examples",
            "Step-by-step tutorials",
            "Technical articles",
        ],

        excluded_topics=[],

        daily_content_limit=5,
    )

    agent = LearningAgent(profile=profile)
    curator = CurationEngine(profile=profile)

    print("Searching the web...")

  


    search_results = agent.run("Find recent educational resources about AI Engineering.")

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
    
    # print("\n" + "=" * 50)
    # print("YOUR AI-CURATED LEARNING FEED")
    # print("=" * 50)

    # for index, topic in enumerate(feed.topics, start=1):

    #     print(f"\n{index}. {topic.title}")

    #     print(f"Description: {topic.description}")

    #     print(f"Source: {topic.source}")

    #     print(f"URL: {topic.url}")

    #     print(
    #         f"Relevance: {topic.relevance_score}/10"
    #     )

    #     print(
    #         f"Learning Value: {topic.learning_value}/10"
    #     )

    #     print(
    #         f"Why recommended: "
    #         f"{topic.reason_for_recommendation}"
    #     )

    #     print("-" * 50)


if __name__ == "__main__":
    main()
