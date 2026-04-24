import logging
from typing import List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.knowledge_base import load_knowledge_base
from app.memory import load_recent_history, save_message


logger = logging.getLogger(__name__)

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


def _fallback_response(message: str, history: List[dict]) -> str:
    """Return a small local answer if the OpenAI request cannot complete."""
    normalized = message.lower()

    if any(term in normalized for term in ["actual policy", "will pay", "guarantee"]):
        return (
            "I cannot confirm whether an actual policy will pay a claim or guarantee a "
            "coverage decision. Claim outcomes depend on the policy contract, policy "
            "status, beneficiary records, exclusions, and the insurer's review. For an "
            "exact answer, contact the insurer or a licensed insurance professional."
        )

    if "summar" in normalized and history:
        topics = [item["content"] for item in history if item["role"] == "user"]
        return (
            "So far, we discussed these life insurance topics: "
            + "; ".join(topics[-3:])
            + ". In general, this is educational information only, and exact coverage "
            "or claim decisions should be confirmed with the insurer."
        )

    if "whole" in normalized:
        return (
            "Whole life insurance is permanent coverage designed to last for the "
            "insured person's lifetime if required premiums are paid. It usually has "
            "a death benefit and a cash value component. It is often more expensive "
            "than term life for the same coverage amount."
        )

    if "universal" in normalized:
        return (
            "Universal life insurance is permanent coverage with flexible premiums "
            "and an adjustable death benefit, subject to policy rules. It can build "
            "cash value, but performance depends on payments, fees, interest crediting, "
            "and policy charges."
        )

    if "claim" in normalized or "document" in normalized or "beneficiary" in normalized:
        return (
            "A beneficiary usually starts a life insurance claim by contacting the "
            "insurer, completing a claim form, and submitting a certified death "
            "certificate. Common documents include the claim form, policy number or "
            "policy document, beneficiary identification, and any trust, estate, or "
            "court documents the insurer requests."
        )

    if "eligible" in normalized or "eligibility" in normalized or "diabetes" in normalized:
        return (
            "Life insurance eligibility varies by insurer and policy. Common factors "
            "include age, health history, tobacco use, occupation, hobbies, residence, "
            "and requested coverage amount. A condition such as diabetes does not "
            "always prevent someone from applying, but it may affect pricing, options, "
            "or approval."
        )

    if "term" in normalized:
        return (
            "Term life insurance provides coverage for a set period, such as 10, 20, "
            "or 30 years. If the insured person dies during the active term and the "
            "claim meets the policy terms, the insurer pays a death benefit to the "
            "named beneficiaries. It is often used for temporary needs like income "
            "replacement, mortgage protection, or support for dependents."
        )

    return (
        "Life insurance generally provides a death benefit to named beneficiaries "
        "when the insured person dies, subject to the policy terms. Common topics "
        "include term life, whole life, universal life, premiums, beneficiaries, "
        "eligibility, underwriting, claims, and required claim documents. This is "
        "general educational information only."
    )


class LifeInsuranceAgent:
    def __init__(self) -> None:
        self.llm: Optional[ChatOpenAI] = None
        if OPENAI_API_KEY:
            try:
                self.llm = ChatOpenAI(
                    openai_api_key=OPENAI_API_KEY,
                    model=OPENAI_MODEL,
                    temperature=0.2,
                )
            except Exception as exc:
                logger.warning(
                    "OpenAI client initialization failed; using local fallback: %s",
                    exc,
                )

    def chat(self, session_id: str, message: str) -> str:
        knowledge_base = load_knowledge_base()
        history = load_recent_history(session_id)
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(knowledge_base=knowledge_base)

        messages = [SystemMessage(content=system_prompt)]
        messages.extend(_history_to_messages(history))
        messages.append(HumanMessage(content=message))

        if self.llm is None:
            response = _fallback_response(message, history)
        else:
            try:
                result = self.llm.invoke(messages)
                response = str(result.content).strip()
            except Exception as exc:
                logger.warning("OpenAI request failed; using local fallback: %s", exc)
                response = _fallback_response(message, history)

        save_message(session_id=session_id, role="user", content=message)
        save_message(session_id=session_id, role="assistant", content=response)

        return response
