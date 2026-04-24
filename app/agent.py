from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.knowledge_base import load_knowledge_base
from app.memory import load_recent_history, save_message


SYSTEM_PROMPT_TEMPLATE = """
You are a Life Insurance Support Assistant.

Use the knowledge base and recent conversation history to answer life insurance
questions clearly and helpfully. Keep answers concise unless the user asks for
detail.

Safety rules:
- Provide general educational information only.
- Do not claim to be a licensed insurance advisor.
- Do not provide legal, financial, medical, tax, or policy-specific advice.
- Do not guarantee eligibility, claim approval, payout amounts, premiums, or
  actual coverage.
- For exact coverage, claim decisions, policy language, or personal advice,
  recommend contacting the insurer, employer benefits administrator, or a
  licensed professional.
- If the user asks about topics outside life insurance support, politely steer
  back to life insurance.

Knowledge base:
{knowledge_base}
""".strip()


def _history_to_messages(history: List[dict]) -> list:
    messages = []
    for item in history:
        if item["role"] == "user":
            messages.append(HumanMessage(content=item["content"]))
        elif item["role"] == "assistant":
            messages.append(AIMessage(content=item["content"]))
    return messages


class LifeInsuranceAgent:
    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not configured. Copy .env.example to .env and set your key."
            )

        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model=OPENAI_MODEL,
            temperature=0.2,
        )

    def chat(self, session_id: str, message: str) -> str:
        knowledge_base = load_knowledge_base()
        history = load_recent_history(session_id)
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(knowledge_base=knowledge_base)

        messages = [SystemMessage(content=system_prompt)]
        messages.extend(_history_to_messages(history))
        messages.append(HumanMessage(content=message))

        result = self.llm.invoke(messages)
        response = str(result.content).strip()

        save_message(session_id=session_id, role="user", content=message)
        save_message(session_id=session_id, role="assistant", content=response)

        return response
