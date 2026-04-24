from pathlib import Path

from app.config import KNOWLEDGE_BASE_PATH


FALLBACK_KNOWLEDGE_BASE = """
Life insurance provides a death benefit to named beneficiaries when the insured
person dies, subject to the terms and exclusions of the policy. Common policy
types include term life, whole life, and universal life insurance. Claimants
usually contact the insurer, submit a claim form, provide a certified death
certificate, and include policy and beneficiary documentation when requested.
This information is general education only and is not legal, financial, medical,
tax, or policy-specific advice.
""".strip()


def load_knowledge_base(path: Path = KNOWLEDGE_BASE_PATH) -> str:
    if not path.exists():
        return FALLBACK_KNOWLEDGE_BASE

    content = path.read_text(encoding="utf-8").strip()
    return content or FALLBACK_KNOWLEDGE_BASE
