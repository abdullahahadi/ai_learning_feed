from app.harness.agent import LearningAgent
from app.profile.schema import LearningProfile



profile = LearningProfile(
    background="Software Developer",
    interests=[
        "AI Engineering",
        "Python",
        "Backend Development",
        "Data Engineering"
    ],
    goals=[
        "Become an AI Engineer",
        "Build AI-powered applications"
    ],
    current_level={
        "Python": "Intermediate",
        "AI Engineering": "Beginner"
    },
    preferred_learning_style=[
        "Practical examples",
        "Step-by-step tutorials",
        "Technical articles"
    ],
    excluded_topics=[],
    daily_content_limit=5
)


agent = LearningAgent(profile=profile)

result = agent.run(
   "Find interesting AI engineering topics for me."
)

print(result)