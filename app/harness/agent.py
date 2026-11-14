from app.profile.schema import LearningProfile
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


class LearningAgent:

    def __init__(self, profile: LearningProfile):
        self.profile = profile
        self.model = "gpt-6-luna"

        

    def run(self, user_input: str) -> str:

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

            tools=[
                {"type": "web_search"}
            ],
            
        )

        return response.output_text