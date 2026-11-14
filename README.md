# AI Learning Feed

AI Learning Feed searches the web for educational resources, curates and ranks them for a learner profile, then delivers the results through a Telegram bot.

## Requirements

- Python
- An OpenAI API key with access to the model configured in `app/harness/agent.py` and the web search tool
- A Telegram bot token and the destination chat ID

## Setup

From the project root, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

The app loads these values from `.env` with `python-dotenv`. Keep your credentials private; `.env` is listed in `.gitignore`.

## Run

From the project root, run:

```powershell
python -m app.main
```

The app uses the sample learner profile and search query in `app/main.py`. It searches the web, asks the model to curate the results into structured topics, ranks them by relevance and learning value, then sends the feed to the configured Telegram chat. It delivers up to the profile's `daily_content_limit`.

Each Telegram topic message includes its description, source URL, relevance score, learning-value score, and reason for recommendation. Edit the profile and search query in `app/main.py` to customize the feed.

## Project layout

```text
app/
  main.py                 # Builds a sample profile and runs the feed pipeline
  profile/
    schema.py             # Learner profile model
  harness/
    agent.py              # Searches the web using the OpenAI Responses API
  tools/
    web_search.py         # Web search tool configuration
  delivery/
    telegram.py           # Sends the curated feed to Telegram
  curation/
    ranker.py             # Curates, scores, ranks, and limits topics
    schema.py             # Structured curated feed and topic models
requirements.txt          # Python dependencies
```
