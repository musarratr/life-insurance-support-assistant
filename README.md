# Life Insurance Support Assistant

A simple Python 3.10+ conversational assistant for general life insurance
support. It uses FastAPI for the backend API, OpenAI through LangChain for
responses, a markdown knowledge base for domain context, SQLite for local
conversation memory, and a basic CLI for chat.

## Features

- Text chat about life insurance policy types, benefits, eligibility, coverage,
  claims, and common claim documents
- OpenAI-powered responses using `langchain-openai`
- Conversation context stored locally in SQLite by `session_id`
- Configurable knowledge base at `data/life_insurance_kb.md`
- FastAPI endpoints for health, chat, and session reset
- CLI chat client for demos and local testing
- Safety guidance for general educational information only

## Architecture

- `app/main.py` exposes the FastAPI application.
- `app/agent.py` builds the LangChain chat workflow and system prompt.
- `app/memory.py` stores and retrieves recent messages from SQLite.
- `app/knowledge_base.py` loads the editable markdown knowledge base.
- `app/config.py` loads environment variables from `.env`.
- `cli.py` sends chat requests to the running API.

## Repository Structure

```text
life-insurance-support-assistant/
├── app/
│   ├── main.py
│   ├── agent.py
│   ├── memory.py
│   ├── knowledge_base.py
│   ├── schemas.py
│   └── config.py
├── data/
│   └── life_insurance_kb.md
├── cli.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── demo_script.md
```

## Setup

Create and activate a virtual environment:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

Edit `.env` and set your real OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
DATABASE_PATH=./life_insurance_assistant.db
KNOWLEDGE_BASE_PATH=./data/life_insurance_kb.md
API_BASE_URL=http://127.0.0.1:8000
```

Do not commit `.env`. It is ignored by git.

## Run the API

```bash
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Run the CLI

In a second terminal with the same virtual environment active:

```bash
python cli.py
```

Use any session ID, or press Enter for `default`. Type `reset` to clear the
current session. Type `exit` or `quit` to leave.

## API Example

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"demo","message":"What is term life insurance?"}'
```

Reset a session:

```bash
curl -X POST http://127.0.0.1:8000/reset/demo
```

## Example Questions

- What is term life insurance?
- How is it different from whole life insurance?
- Who is usually eligible for life insurance?
- Can someone with diabetes apply?
- How does a beneficiary file a claim?
- What documents are usually required?
- Can you summarize what we discussed about term life?
- Can you confirm whether my actual policy will pay my family?

## Limitations and Safety

This assistant provides general educational information only. It is not a
licensed insurance advisor and does not provide legal, financial, tax, medical,
or policy-specific advice. It cannot guarantee eligibility, premiums, coverage,
claim approval, or payout amounts. For exact coverage, claim decisions, or
personal advice, contact the insurer, employer benefits administrator, or a
licensed professional.

## Demo Video Instructions

For a 3 to 5 minute demo, show:

1. The repository structure and `.env.example`.
2. The FastAPI server starting with `uvicorn app.main:app --reload`.
3. The CLI starting with `python cli.py`.
4. A few life insurance questions across the same session.
5. A follow-up question that proves conversation memory works.
6. A policy-specific question where the assistant avoids making guarantees.
