# AI Learning Feed

A small Python application that uses the OpenAI API and web search to find AI engineering learning topics, personalized with a learner profile.

## Requirements

- Python
- An OpenAI API key with access to the configured model and web search

## Setup

From the project root, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root and add your API key:

```dotenv
OPENAI_API_KEY=your_api_key
```

Keep the key private. The `.env` file is listed in `.gitignore`.

## Run

Run the app from the project root:

```powershell
python -m app.main
```

The app constructs a sample learning profile, asks for interesting AI engineering topics, and prints the response. The model name and sample profile are currently set in the source code.

## Project layout

```text
app/
  main.py             # Creates the sample profile and runs the agent
  harness/
    agent.py          # Calls the OpenAI Responses API with web search
  profile/
    schema.py         # LearningProfile data model
requirements.txt      # Python dependencies
```
