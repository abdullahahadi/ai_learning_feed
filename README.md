# AI Learning Feed

AI Learning Feed searches the web for educational resources, curates and ranks them for a learner profile, then delivers the results through a Telegram bot.

## Architecture

The target design, the rules that keep its parts separate, and the roadmap are described in [docs/architecture.md](docs/architecture.md).

## Requirements

- Python 3.14+ and `uv` to run locally, or Docker to run in a container
- An OpenAI API key with access to the model configured in `src/ai_learning_feed/harness/agent.py` and the web search tool
- A Telegram bot token and the destination chat ID

## Configuration

Create a `.env` file in the project root for either run option:

```dotenv
OPENAI_API_KEY=your_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

The app loads these values from `.env` with `python-dotenv`. Keep your credentials private; `.env` is listed in `.gitignore`.

## Run locally with uv

Install the project and its dependencies, then run it from the project root:

```powershell
uv sync
uv run python -m ai_learning_feed.main
```

## Type checking

The project uses [ty](https://docs.astral.sh/ty/) to check type hints without running the code:

```powershell
uv run ty check
```

## Pre-commit hooks

Install the Git hooks with:

```powershell
uv run pre-commit install
```

The hooks keep `uv.lock` up to date, run Ruff checks with `--fix`, and format code with Ruff.

## Run with Docker

Build the image from the project root:

```powershell
docker build -t ai-learning-feed .
```

Run the container with your `.env` file. The file is passed at runtime and is not included in the image:

```powershell
docker run --rm --env-file .env ai-learning-feed
```

The app uses the sample learner profile and search query in `src/ai_learning_feed/main.py`. It searches the web, asks the model to curate the results into structured topics, ranks them by relevance and learning value, then sends the feed to the configured Telegram chat. It delivers up to the profile's `daily_content_limit`.

Each Telegram topic message includes its description, source URL, relevance score, learning-value score, and reason for recommendation. Edit the profile and search query in `src/ai_learning_feed/main.py` to customize the feed.

## Project layout

```text
src/
  ai_learning_feed/
    __init__.py
    main.py               # Builds a sample profile and runs the feed pipeline
    profile/
      schema.py           # Learner profile model
    harness/
      agent.py            # Searches the web using the OpenAI Responses API
    tools/
      web_search.py       # Web search tool configuration
    delivery/
      telegram.py         # Sends the curated feed to Telegram
    curation/
      ranker.py           # Curates, scores, ranks, and limits topics
      schema.py           # Structured curated feed and topic models
Dockerfile                # Container image definition
.dockerignore             # Files excluded from the Docker build context
pyproject.toml            # Project metadata and dependencies
uv.lock                   # Locked dependency versions
```
