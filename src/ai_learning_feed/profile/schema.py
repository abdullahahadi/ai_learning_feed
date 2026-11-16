from pydantic import BaseModel


class LearningProfile(BaseModel):
    background: str
    interests: list[str]
    goals: list[str]
    current_level: dict[str, str]
    preferred_learning_style: list[str]
    excluded_topics: list[str]
    daily_content_limit: int = 5
