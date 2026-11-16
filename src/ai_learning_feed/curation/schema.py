from pydantic import BaseModel, Field


class CuratedTopic(BaseModel):
    title: str
    description: str
    url: str
    source: str
    relevance_score: int = Field(ge=1, le=10)
    learning_value: int = Field(ge=1, le=10)
    reason_for_recommendation: str


class CuratedFeed(BaseModel):
    topics: list[CuratedTopic]
