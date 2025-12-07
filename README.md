# Chat Aggregator

Aggregates and summarizes unread messages from multiple chat platforms (Slack, MS Teams, Email) and extracts actionable insights.

## Features

- Fetches messages from multiple platforms
- Categorizes content into:
  - **Action Items** with urgency levels (HIGH/MEDIUM/LOW)
  - **Key Decisions** made by the team
  - **Questions Awaiting Response**
  - **Meetings & Calendar Events** (existing + suggested)
- Fact-checking loop to verify summary accuracy

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- Gemini API key from https://aistudio.google.com/apikey

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/divyumsinghal/chat-aggregator.git
   cd chat-aggregator
   ```

2. Create virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

3. Create `.env` file in `chat_assistant/` with your Gemini API key:
   ```bash
   echo "GOOGLE_GENAI_USE_VERTEXAI=0" > chat_assistant/.env
   echo "GOOGLE_API_KEY=your_api_key_here" >> chat_assistant/.env
   ```

## Running the Agent

Start the ADK web interface:
```bash
source .venv/bin/activate
adk web --port 8000
```

Open http://127.0.0.1:8000 in your browser and select the `chat_assistant` agent.

Try prompts like:
- "Tell me what I've missed"
- "Summarize my unread messages"
- "What needs my attention today?"

## Project Structure

```
chat_assistant/
├── agent.py        # Agent definitions and orchestration
├── utils.py        # Tools for fetching chat data
└── mock_data.json  # Sample chat data for testing
```

## Testing with Mock Data

The project includes `mock_data.json` with sample messages. To use your own data, update the JSON file with your chat exports.
