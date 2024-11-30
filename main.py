from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


from crewAI.crew import pharma_chat
# from twilio_integration.twilio import create_and_send_conversation

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

# @app.post("/send-conversation-link/{phone_number}")
# async def send_conversation(phone_number: str):
#     try:
#         response = create_and_send_conversation(phone_number,use_whatsapp=False, use_ultramsg = False, use_textbelt=True)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))