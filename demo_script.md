# Demo Script

Use this script for a 3 to 5 minute walkthrough video.

## 1. Introduce the Project

"This is a simple Life Insurance Support Assistant built with Python, Streamlit,
FastAPI, OpenAI, LangChain, SQLite memory, and a configurable markdown knowledge
base."

Show the repository structure and point out:

- `app/main.py` for the API
- `app/agent.py` for the LangChain assistant workflow
- `app/memory.py` for SQLite conversation memory
- `data/life_insurance_kb.md` for editable insurance knowledge
- `streamlit_app.py` for the web chat interface
- `cli.py` for text chat

## 2. Start the Streamlit Chat Interface

Run:

```bash
source .venv/bin/activate
streamlit run streamlit_app.py
```

Use session ID:

```text
demo
```

## 3. Ask Example Questions

Ask these questions in order in the Streamlit chat box:

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

## 4. Show Conversation Memory

Ask:

```text
Can you summarize what we discussed about term life?
```

Point out that the assistant uses the same session ID and SQLite memory to keep
recent conversation context.

## 5. Show Safe-Answer Behavior

Ask:

```text
Can you confirm whether my actual policy will pay my family?
```

Expected behavior: the assistant should avoid guaranteeing a claim or coverage
decision and recommend contacting the insurer or a licensed professional for the
specific policy.

## 6. Reset the Session

Click `Reset Chat` in the sidebar.

Explain that this clears the current SQLite conversation history for the demo
session.

## 7. Optional API and CLI Check

If time allows, show the alternate interfaces:

```bash
uvicorn app.main:app --reload
```

```bash
python cli.py
```
