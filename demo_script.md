# Streamlit Demo Script

Use this script for a practical 4 to 6 minute video demo of the Life Insurance
Support Assistant.

## 1. Opening

Say:

"This is a Life Insurance Support Assistant. It uses Streamlit for the web chat
interface, OpenAI through LangChain for responses, SQLite for conversation
memory, and a markdown knowledge base for life insurance context."

Show the repository root and briefly point out:

- `streamlit_app.py` for the web chat interface
- `app/agent.py` for the OpenAI and LangChain chat workflow
- `app/memory.py` for SQLite conversation memory
- `data/life_insurance_kb.md` for editable life insurance knowledge
- `.env.example` for required environment variables
- `README.md` for setup and usage instructions

## 2. Confirm Environment Setup

Show that the virtual environment is active, or activate it:

```bash
source .venv/bin/activate
```

Show the dependency install command:

```bash
pip install -r requirements.txt
```

Say:

"The `.env` file contains my local OpenAI API key and configuration. I will not
show the API key on screen. The project includes `.env.example` so another user
can create their own local `.env` file."

Optionally show `.env.example`:

```bash
cat .env.example
```

## 3. Launch the Streamlit App

Run the app with one command:

```bash
streamlit run streamlit_app.py
```

Say:

"This starts the local Streamlit chat interface. The app uses the existing
assistant code directly, so I do not need to start the FastAPI server for this
demo."

Open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## 4. Show the Chat Interface

On the Streamlit page, point out:

- The main chat area
- The `Session ID` field in the sidebar
- The `Reset Chat` button
- The short safety note: "General educational information only."

Set the session ID to:

```text
demo
```

Say:

"The session ID is used to store and retrieve conversation history from SQLite.
Using the same session ID keeps context across turns."

## 5. Ask Basic Life Insurance Questions

Ask the first question:

```text
What is term life insurance?
```

After the answer appears, say:

"The assistant explains term life insurance using the configured knowledge base
and the OpenAI model."

Ask:

```text
How is it different from whole life insurance?
```

Say:

"This follow-up question depends on the previous topic, and the assistant can
continue the conversation naturally."

## 6. Ask Eligibility Questions

Ask:

```text
Who is usually eligible for life insurance?
```

Then ask:

```text
Can someone with diabetes apply?
```

Say:

"The assistant gives general educational information. It does not make a medical
or underwriting decision, and it avoids guaranteeing approval."

## 7. Ask Claims Questions

Ask:

```text
How does a beneficiary file a claim?
```

Then ask:

```text
What documents are usually required?
```

Say:

"The assistant covers the typical claims process and common documents, such as a
claim form, certified death certificate, policy information, and beneficiary
identification."

## 8. Demonstrate Conversation Memory

Ask:

```text
Can you summarize what we discussed about term life?
```

Say:

"This demonstrates conversation memory. The app loads recent messages for the
same session ID from SQLite and includes them in the LangChain message history."

## 9. Demonstrate Safe-Answer Behavior

Ask:

```text
Can you confirm whether my actual policy will pay my family?
```

Expected behavior:

The assistant should not guarantee a claim outcome or policy-specific coverage.
It should explain that actual decisions depend on the policy contract, insurer
review, exclusions, policy status, and documentation. It should recommend
contacting the insurer or a licensed professional.

Say:

"This is an important safety behavior. The assistant provides general education,
but it does not claim to be a licensed insurance advisor and does not make
policy-specific guarantees."

## 10. Reset the Chat

Click `Reset Chat` in the sidebar.

Say:

"Reset Chat clears the SQLite conversation history for this session ID."

Ask a short question again, such as:

```text
What is term life insurance?
```

Say:

"After reset, the app starts a fresh conversation for the same session."

## 11. Closing

Say:

"That completes the demo. The Streamlit app provides the main user-friendly chat
interface, while the project also includes FastAPI and CLI entry points for
testing or integration. The implementation stays intentionally simple: OpenAI
and LangChain for responses, a markdown knowledge base for domain context, and
SQLite for local memory."

Stop the Streamlit server with:

```text
Ctrl+C
```
