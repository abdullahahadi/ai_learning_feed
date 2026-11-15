from ai_learning_feed.profile.schema import LearningProfile
from ai_learning_feed.tools.web_search import WEB_SEARCH_TOOL
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


class LearningAgent:
    """Search the web for learning resources relevant to a learner profile."""

    def __init__(self, profile: LearningProfile):
        self.profile = profile
        self.model = "gpt-6-luna"

        

    def run(self, user_input: str) -> str:
        """Return web-search results for the supplied query."""
        profile_context = self.profile.model_dump_json(indent=2)

        response = client.responses.create(
            model=self.model,
            instructions=f"""
            You are a personalized AI learning curator.

            Use the following user profile to personalize
            your research and recommendations.

            USER PROFILE:
            {profile_context}

            Prioritize relevant, high-quality educational
            content matching the user's goals.
            """,

            input=user_input,

            tools=[WEB_SEARCH_TOOL],
            
        )

        return response.output_text