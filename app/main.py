from typing import Optional

from fastapi import FastAPI, HTTPException

from app.agent import LifeInsuranceAgent
from app.memory import clear_session, init_db
from app.schemas import ChatRequest, ChatResponse


app = FastAPI(
    title="Life Insurance Support Assistant",
    description="A simple FastAPI backend for life insurance support chat.",
    version="1.0.0",
)

_agent: Optional[LifeInsuranceAgent] = None


@app.on_event("startup")
def startup() -> None:
    init_db()


def get_agent() -> LifeInsuranceAgent:
    global _agent
    if _agent is None:
        _agent = LifeInsuranceAgent()
    return _agent


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = get_agent().chat(
            session_id=request.session_id,
            message=request.message,
        )
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate a response. Check the server logs and configuration.",
        ) from exc

    return ChatResponse(session_id=request.session_id, response=response)


@app.post("/reset/{session_id}")
def reset(session_id: str) -> dict:
    clear_session(session_id)
    return {"session_id": session_id, "status": "cleared"}
