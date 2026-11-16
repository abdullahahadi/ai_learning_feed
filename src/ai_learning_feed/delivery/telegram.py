import os

import requests
from dotenv import load_dotenv

load_dotenv()


class TelegramSender:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.token or not self.chat_id:
            raise ValueError("Telegram credentials are missing.")

        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, message: str):

        response = requests.post(
            self.api_url, json={"chat_id": self.chat_id, "text": message}, timeout=15
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("ok"):
            raise RuntimeError(result)

        return result

    def send_feed(self, feed):

        header = "🧠 YOUR AI-CURATED LEARNING FEED\n\n"

        self.send_message(header)

        for index, topic in enumerate(feed.topics, start=1):
            message = (
                f"📚 {index}. {topic.title}\n\n"
                f"{topic.description}\n\n"
                f"🔗 {topic.url}\n\n"
                f"⭐ Relevance: {topic.relevance_score}/10\n"
                f"🎯 Learning value: {topic.learning_value}/10\n\n"
                f"💡 Why recommended:\n"
                f"{topic.reason_for_recommendation}"
            )

            self.send_message(message)
