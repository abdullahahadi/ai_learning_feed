import pytest

from ai_learning_feed.curation.schema import CuratedFeed, CuratedTopic
from ai_learning_feed.profile.schema import LearningProfile


@pytest.fixture
def learning_profile():
    return LearningProfile(
        background="Software developer",
        interests=["Python"],
        goals=["Learn practical Python"],
        current_level={"Python": "Intermediate"},
        preferred_learning_style=["Tutorials"],
        excluded_topics=[],
    )


@pytest.fixture
def curated_topic():
    return CuratedTopic(
        title="Python tutorial",
        description="A practical introduction to Python.",
        url="https://example.com/python",
        source="Example",
        relevance_score=8,
        learning_value=9,
        reason_for_recommendation="It includes practical exercises.",
    )


@pytest.fixture
def curated_feed(curated_topic):
    return CuratedFeed(topics=[curated_topic])
