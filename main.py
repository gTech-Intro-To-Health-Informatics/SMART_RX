from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from crewAI.crew import pharma_chat

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


class ChatRequest(BaseModel):
    drug_list: List[str]
    patient_history: str
    conversation_history: List[dict]  # List of messages with 'role' and 'content'
    patient_query: str

class ChatResponse(BaseModel):
    conversation_history: List[dict]

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    updated_conversation = pharma_chat(
        drug_list=chat_request.drug_list,
        patient_history=chat_request.patient_history,
        conversation_history=chat_request.conversation_history,
        patient_query=chat_request.patient_query
    )
    return ChatResponse(conversation_history=updated_conversation)
