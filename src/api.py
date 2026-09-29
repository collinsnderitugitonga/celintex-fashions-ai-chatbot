from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.chatbot import answer_question


app = FastAPI(
    title="Celintex Fashion AI API",
    description="Backend API for the Celintex AI Fashion Assistant",
    version="1.0.0"
)


# Allow the website to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Celintex Fashion AI API is running."
    }


@app.post("/api/chat")
def chat(request: ChatRequest):
    response = answer_question(request.message)

    return {
        "response": response
    }
