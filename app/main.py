"""Minimal API: uvicorn app.main:app --reload"""
import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import chat_turn

app = FastAPI(title="Hyderabad Food Finder")
SESSIONS: dict[str, list[dict]] = {}  # in-memory, dev only


class ChatIn(BaseModel):
    message: str
    session_id: str | None = None


class ChatOut(BaseModel):
    session_id: str
    reply: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/chat", response_model=ChatOut)
def chat(body: ChatIn) -> ChatOut:
    sid = body.session_id or str(uuid.uuid4())
    history = SESSIONS.setdefault(sid, [])
    history.append({"role": "user", "content": body.message})
    reply = chat_turn(history)
    return ChatOut(session_id=sid, reply=reply)
