from ai_learning_feed.profile.schema import LearningProfile


def build_sample_profile() -> LearningProfile:
    """Return the example learner profile used by the app."""
    return LearningProfile(
        background="Software Developer",
        interests=[
            "Python",
            "Python Scripts",
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
            "YouTube videos",
        ],
        excluded_topics=[],
        daily_content_limit=5,
    )
