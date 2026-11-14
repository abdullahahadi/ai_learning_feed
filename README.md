# AI Learning Feed

AI Learning Feed searches the web for educational resources and creates a personalized, ranked learning feed using an OpenAI model.

## Requirements

- Python
- An OpenAI API key with access to the model configured in `app/harness/agent.py` and the web search tool

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
```

The app loads this file with `python-dotenv`. Keep the API key private; `.env` is listed in `.gitignore`.

## Run

From the project root, run:

```powershell
python -m app.main
```

The app uses the sample learner profile and search query in `app/main.py`. It searches the web, asks the model to curate the results into structured topics, ranks them using relevance and learning-value scores, and prints up to the profile's `daily_content_limit`.

Each printed topic includes its description, source URL, relevance score, learning-value score, and reason for recommendation. Edit the profile and search query in `app/main.py` to customize the feed.

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
  curation/
    ranker.py             # Curates, scores, ranks, and limits topics
    schema.py             # Structured curated feed and topic models
requirements.txt          # Python dependencies
```
