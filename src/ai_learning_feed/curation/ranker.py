
from openai import OpenAI

from ai_learning_feed.profile.schema import LearningProfile
from ai_learning_feed.curation.schema import CuratedFeed

client = OpenAI()


class CurationEngine:
    """Turn web-search results into a personalized, ranked learning feed."""

    def __init__(self, profile: LearningProfile):
        self.profile = profile
        self.model = "gpt-6-luna"

    def curate(
        self,
        search_results: str,
        limit: int = 5
    ) -> CuratedFeed:
        """Curate search results and return at most ``limit`` ranked topics."""
        profile_context = self.profile.model_dump_json(
            indent=2
        )

        response = client.responses.parse(
            model=self.model,

            instructions=f"""
            You are an expert AI learning curator.

            USER PROFILE:
            {profile_context}

            Evaluate the supplied search results.

            For each topic:
            - Assess relevance to the user's interests.
            - Assess educational and practical value.
            - Explain why it is recommended.
            - Preserve the original source URL.
            - Avoid duplicate topics.
            - Exclude irrelevant or low-quality content.

            relevance_score: 1 to 10
            learning_value: 1 to 10

            Return the most valuable topics.
            """,

            input=f"""
            Evaluate and curate these search results.

            Return no more than {limit} topics.

            SEARCH RESULTS:
            {search_results}
            """,

            text_format=CuratedFeed,
        )

        feed = response.output_parsed

        if feed is None:
            raise ValueError("Could not parse curated feed")

        feed.topics.sort(
            key=lambda topic: (
                # Relevance carries more weight than learning value.
                topic.relevance_score * 0.6
                + topic.learning_value * 0.4
            ),
            reverse=True,
        )

        feed.topics = feed.topics[:limit]

        return feed
