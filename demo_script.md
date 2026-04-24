# Demo Script

Use this script for a 3 to 5 minute walkthrough video.

## 1. Introduce the Project

"This is a simple Life Insurance Support Assistant built with Python, FastAPI,
OpenAI, LangChain, SQLite memory, and a configurable markdown knowledge base."

Show the repository structure and point out:

- `app/main.py` for the API
- `app/agent.py` for the LangChain assistant workflow
- `app/memory.py` for SQLite conversation memory
- `data/life_insurance_kb.md` for editable insurance knowledge
- `cli.py` for text chat

## 2. Start the API

Run:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Open or mention:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## 3. Start the CLI

In a second terminal, run:

```bash
source .venv/bin/activate
python cli.py
```

Use session ID:

```text
demo
```

## 4. Ask Example Questions

Ask these questions in order:

```text
What is term life insurance?
```

```text
How is it different from whole life insurance?
```

```text
Who is usually eligible for life insurance?
```

```text
Can someone with diabetes apply?
```

```text
How does a beneficiary file a claim?
```

```text
What documents are usually required?
```

## 5. Show Conversation Memory

Ask:

```text
Can you summarize what we discussed about term life?
```

Point out that the assistant uses the same session ID and SQLite memory to keep
recent conversation context.

## 6. Show Safe-Answer Behavior

Ask:

```text
Can you confirm whether my actual policy will pay my family?
```

Expected behavior: the assistant should avoid guaranteeing a claim or coverage
decision and recommend contacting the insurer or a licensed professional for the
specific policy.

## 7. Reset the Session

Run this CLI command:

```text
reset
```

Explain that this clears the current SQLite conversation history for the demo
session.
